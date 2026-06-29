#!/usr/bin/env python3
"""
add_publication.py
------------------
向 stair-team Hugo 主页添加或更新论文发表信息。

支持从 ACL Anthology 自动获取元信息，可同时提供 arXiv ID 以合并 arXiv 版本。

用法示例:
  # 通过 ACL Anthology ID
  python scripts/add_publication.py 2026.acl-long.1471

  # 通过 ACL Anthology URL
  python scripts/add_publication.py https://aclanthology.org/2026.acl-long.1471/

  # 同时提供 arXiv ID（用于获取摘要或合并已有 arXiv 条目）
  python scripts/add_publication.py 2026.acl-long.1471 --arxiv 2601.12906

  # 提供代码/网站链接
  python scripts/add_publication.py 2026.acl-long.1471 --arxiv 2601.12906 \\
      --code https://github.com/org/repo --website https://project.page

  # 仅预览，不写入文件
  python scripts/add_publication.py 2026.acl-long.1471 --dry-run
"""

import argparse
import os
import re
import sys
import textwrap
import urllib.request
import urllib.error
from pathlib import Path

# ---------------------------------------------------------------------------
# 路径配置
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLICATION_DIR = REPO_ROOT / "content" / "publication"

# ---------------------------------------------------------------------------
# Venue 映射：将 ACL Anthology booktitle 规范化
# ---------------------------------------------------------------------------
VENUE_PATTERNS = [
    # ACL
    (r"Annual Meeting of the Association for Computational Linguistics.*Volume 1.*Long",
     "ACL", "main", "Proc. of the Association for Computational Linguistics, ACL Main"),
    (r"Annual Meeting of the Association for Computational Linguistics.*Volume 2.*Short",
     "ACL", "short", "Proc. of the Association for Computational Linguistics, ACL Short"),
    (r"Findings of the Association for Computational Linguistics: ACL",
     "ACL", "findings", "Findings of the Association for Computational Linguistics: ACL"),
    # EMNLP
    (r"Empirical Methods in Natural Language Processing.*(?!Findings)",
     "EMNLP", "main", "Proc. of the Empirical Methods in Natural Language Processing, EMNLP Main"),
    (r"Findings of the Association for Computational Linguistics: EMNLP",
     "EMNLP", "findings", "Findings of the Association for Computational Linguistics: EMNLP"),
    # NAACL
    (r"North American Chapter of the Association for Computational Linguistics.*(?!Findings)",
     "NAACL", "main", "Proc. of the North American Chapter of the Association for Computational Linguistics, NAACL"),
    (r"Findings of the Association for Computational Linguistics: NAACL",
     "NAACL", "findings", "Findings of the Association for Computational Linguistics: NAACL"),
    # EACL
    (r"European Chapter of the Association for Computational Linguistics",
     "EACL", "main", "Proc. of the European Chapter of the Association for Computational Linguistics, EACL"),
    # COLING
    (r"International Conference on Computational Linguistics|COLING",
     "COLING", "main", "Proc. of the International Conference on Computational Linguistics, COLING"),
    # ICLR
    (r"International Conference on Learning Representations|ICLR",
     "ICLR", "main", "International Conference on Learning Representations, ICLR"),
    # NeurIPS / NIPS
    (r"Neural Information Processing Systems|NeurIPS|NIPS",
     "NeurIPS", "main", "Advances in Neural Information Processing Systems, NeurIPS"),
    # ICML
    (r"International Conference on Machine Learning|ICML",
     "ICML", "main", "Proc. of the International Conference on Machine Learning, ICML"),
    # AAAI
    (r"AAAI Conference on Artificial Intelligence|Association for the Advancement of Artificial Intelligence",
     "AAAI", "main", "Proc. of the AAAI Conference on Artificial Intelligence, AAAI"),
    # IJCAI
    (r"International Joint Conference on Artificial Intelligence|IJCAI",
     "IJCAI", "main", "Proc. of the International Joint Conference on Artificial Intelligence, IJCAI"),
    # KDD
    (r"ACM SIGKDD|Knowledge Discovery and Data Mining",
     "KDD", "main", "Proc. of the ACM SIGKDD Conference on Knowledge Discovery and Data Mining, KDD"),
    # WWW
    (r"World Wide Web Conference|The Web Conference|WWW",
     "WWW", "main", "Proc. of the World Wide Web Conference, WWW"),
    # WSDM
    (r"Web Search and Data Mining|WSDM",
     "WSDM", "main", "Proc. of the ACM International Conference on Web Search and Data Mining, WSDM"),
    # CIKM
    (r"Information and Knowledge Management|CIKM",
     "CIKM", "main", "Proc. of the ACM International Conference on Information and Knowledge Management, CIKM"),
    # ECML-PKDD
    (r"European Conference on Machine Learning|ECML",
     "ECML-PKDD", "main", "Proc. of the European Conference on Machine Learning, ECML-PKDD"),
    # SDM
    (r"SIAM International Conference on Data Mining|SDM",
     "SDM", "main", "Proc. of the SIAM International Conference on Data Mining, SDM"),
    # PAKDD
    (r"Pacific-Asia Conference on Knowledge Discovery|PAKDD",
     "PAKDD", "main", "Proc. of the Pacific-Asia Conference on Knowledge Discovery and Data Mining, PAKDD"),
    # ICDM
    (r"IEEE International Conference on Data Mining|ICDM",
     "ICDM", "main", "Proc. of the IEEE International Conference on Data Mining, ICDM"),
    # ACL Anthology generic fallback
    (r"Association for Computational Linguistics",
     "ACL", "other", "Proc. of the Association for Computational Linguistics"),
]


def detect_venue(booktitle: str) -> tuple[str, str, str]:
    """返回 (venue_short, track, publication_string)"""
    for pattern, venue, track, pub_str in VENUE_PATTERNS:
        if re.search(pattern, booktitle, re.IGNORECASE):
            return venue, track, pub_str
    return "Conference", "main", booktitle


# ---------------------------------------------------------------------------
# BibTeX 简易解析（仅用于 ACL Anthology 的规范格式）
# ---------------------------------------------------------------------------
def parse_bibtex(bib_text: str) -> dict:
    """从 BibTeX 文本提取字段，返回 dict。"""
    fields = {}

    # 提取 entry key
    m = re.match(r'\s*@\w+\{([^,]+),', bib_text)
    if m:
        fields["_key"] = m.group(1).strip()

    # 提取所有 field = {value} 或 field = "value"
    for m in re.finditer(
        r'(\w+)\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|"([^"]*)")',
        bib_text,
        re.DOTALL,
    ):
        key = m.group(1).lower()
        val = (m.group(2) or m.group(3) or "").strip()
        val = re.sub(r'\s+', ' ', val)
        # 去除 LaTeX 花括号（保留内容）
        val = re.sub(r'\{([^}]*)\}', r'\1', val)
        fields[key] = val

    return fields


def parse_authors_bibtex(author_str: str) -> list[str]:
    """解析 BibTeX author 字段，返回 'Firstname Lastname' 列表。"""
    authors = []
    for part in re.split(r'\s+and\s+', author_str, flags=re.IGNORECASE):
        part = part.strip()
        if not part:
            continue
        # "Last, First" → "First Last"
        if ',' in part:
            last, first = part.split(',', 1)
            authors.append(f"{first.strip()} {last.strip()}")
        else:
            authors.append(part)
    return authors


# ---------------------------------------------------------------------------
# 网络请求工具
# ---------------------------------------------------------------------------
def fetch_url(url: str, timeout: int = 10) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  [warn] 无法获取 {url}: {e}", file=sys.stderr)
        return None


def fetch_acl_bibtex(acl_id: str) -> dict | None:
    """从 ACL Anthology 获取 BibTeX 并解析。"""
    url = f"https://aclanthology.org/{acl_id}.bib"
    print(f"  获取 BibTeX: {url}")
    content = fetch_url(url)
    if not content or "@" not in content:
        return None
    return parse_bibtex(content)


def fetch_acl_abstract(acl_id: str) -> str | None:
    """从 ACL Anthology 页面抓取摘要。"""
    url = f"https://aclanthology.org/{acl_id}/"
    print(f"  获取摘要（ACL Anthology）: {url}")
    html = fetch_url(url)
    if not html:
        return None
    m = re.search(
        r'<div[^>]*class="[^"]*card-body[^"]*acl-abstract[^"]*"[^>]*>(.*?)</div>',
        html, re.DOTALL | re.IGNORECASE
    )
    if not m:
        # 备用：寻找 Abstract 段落
        m = re.search(
            r'<span[^>]*id="abstract"[^>]*>(.*?)</span>', html, re.DOTALL | re.IGNORECASE
        )
    if m:
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        text = re.sub(r'\s+', ' ', text)
        # 去除页面自动添加的 "Abstract" 前缀
        text = re.sub(r'^Abstract\s*', '', text, flags=re.IGNORECASE)
        return text.strip()
    return None


def fetch_arxiv_abstract(arxiv_id: str) -> str | None:
    """从 arXiv 获取摘要。"""
    url = f"https://arxiv.org/abs/{arxiv_id}"
    print(f"  获取摘要（arXiv）: {url}")
    html = fetch_url(url)
    if not html:
        return None
    m = re.search(
        r'<blockquote[^>]*class="abstract[^"]*"[^>]*>(.*?)</blockquote>',
        html, re.DOTALL | re.IGNORECASE
    )
    if m:
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        text = re.sub(r'^\s*Abstract:\s*', '', text, flags=re.IGNORECASE)
        return re.sub(r'\s+', ' ', text)
    return None


# ---------------------------------------------------------------------------
# 目录名生成
# ---------------------------------------------------------------------------
def make_slug(title: str, max_len: int = 60) -> str:
    """将标题转换为小写字母数字连续字符串，最长 max_len。"""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9]+', '', slug)
    return slug[:max_len]


def make_dir_name(venue: str, year: str, title: str) -> str:
    return f"{venue}-{year}-{make_slug(title)}"


# ---------------------------------------------------------------------------
# 查找已有的 arXiv 版本
# ---------------------------------------------------------------------------
def find_existing_arxiv_entry(title: str, arxiv_id: str | None = None) -> Path | None:
    """
    在 content/publication 中查找可能对应的 arXiv 条目。
    匹配策略：
      1. 如果提供了 arxiv_id，在文件内容中搜索该 ID
      2. 基于标题关键词匹配目录名（至少匹配前3个关键词）
    """
    if not PUBLICATION_DIR.exists():
        return None

    # 策略1：按 arXiv ID 搜索文件内容
    if arxiv_id:
        arxiv_clean = arxiv_id.replace(".", "").replace("/", "")
        for d in PUBLICATION_DIR.iterdir():
            if not d.is_dir():
                continue
            idx = d / "index.md"
            if idx.exists() and arxiv_clean in idx.read_text():
                print(f"  发现已有 arXiv 条目（按ID匹配）: {d.name}")
                return d

    # 策略2：按标题关键词匹配目录名
    keywords = [w.lower() for w in re.findall(r'[a-zA-Z]{3,}', title)][:5]
    for d in PUBLICATION_DIR.iterdir():
        if not d.is_dir() or not d.name.startswith("arxiv"):
            continue
        dir_lower = d.name.lower()
        matched = sum(1 for kw in keywords if kw in dir_lower)
        if matched >= 3:
            print(f"  发现已有 arXiv 条目（按标题匹配，{matched}/{len(keywords)} 关键词）: {d.name}")
            return d

    return None


# ---------------------------------------------------------------------------
# Hugo front-matter 生成
# ---------------------------------------------------------------------------
def escape_yaml_string(s: str) -> str:
    """将字符串安全地格式化为 YAML 双引号字符串内容。"""
    return s.replace('\\', '\\\\').replace('"', '\\"')


def build_publication_string(pub_str: str, year: str, pages: str | None) -> str:
    """构造 publication 字段内容。"""
    result = f"*{pub_str}, {year}"
    if pages:
        pages_clean = pages.replace("--", "–")
        result += f", pages {pages_clean}"
    result += "*"
    return result


def render_index_md(
    title: str,
    authors: list[str],
    venue: str,
    track: str,
    pub_str: str,
    year: str,
    month: str,
    pages: str | None,
    doi: str | None,
    acl_url: str,
    acl_pdf_url: str,
    arxiv_id: str | None,
    code_url: str | None,
    website_url: str | None,
    abstract: str | None,
) -> str:
    lines = ["---"]
    # 标题：含单引号时用双引号包裹，否则用单引号
    if "'" in title:
        lines.append(f'title: "{escape_yaml_string(title)}"')
    else:
        lines.append(f"title: '{title}'")

    lines.append("authors:")
    for a in authors:
        lines.append(f"- {a}")

    # 日期（取 7 月 1 日作为会议月份）
    month_num = {
        "january": "01", "february": "02", "march": "03", "april": "04",
        "may": "05", "june": "06", "july": "07", "august": "08",
        "september": "09", "october": "10", "november": "11", "december": "12",
        "jan": "01", "feb": "02", "mar": "03", "apr": "04",
        "jun": "06", "jul": "07", "aug": "08", "sep": "09",
        "oct": "10", "nov": "11", "dec": "12",
    }.get(month.lower(), "07") if month else "07"
    lines.append(f"date: '{year}-{month_num}-01'")
    lines.append(f"publishDate: '{year}-{month_num}-01T00:00:00Z'")

    lines.append("publication_types:")
    lines.append("- paper-conference")

    pub_field = build_publication_string(pub_str, year, pages)
    lines.append(f"publication: '{pub_field}'")

    if doi:
        lines.append(f"doi: {doi}")

    if abstract:
        lines.append(f'abstract: "{escape_yaml_string(abstract)}"')

    lines.append("")
    lines.append("featured: false")
    lines.append("")
    lines.append("links:")
    lines.append(f"- name: ACL Anthology")
    lines.append(f"  url: {acl_url}")
    if arxiv_id:
        lines.append(f"- name: arXiv")
        lines.append(f"  url: https://arxiv.org/abs/{arxiv_id}")
    if code_url:
        lines.append(f"- name: Code")
        lines.append(f"  url: {code_url}")
    if website_url:
        lines.append(f"- name: Website")
        lines.append(f"  url: {website_url}")
    lines.append("")
    lines.append(f"url_pdf: '{acl_pdf_url}'")
    if code_url:
        lines.append(f"url_code: '{code_url}'")
    lines.append("")
    lines.append("image:")
    lines.append("  caption: ''")
    lines.append("  focal_point: ''")
    lines.append("  placement: 2")
    lines.append("  preview_only: false")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def normalize_acl_id(raw: str) -> str:
    """从 URL 或裸 ID 中提取 ACL Anthology ID。"""
    raw = raw.strip().rstrip("/")
    # https://aclanthology.org/2026.acl-long.1471
    m = re.search(r'aclanthology\.org/([^/]+?)(?:\.bib|\.pdf|\.html)?$', raw)
    if m:
        return m.group(1)
    # 直接是 ID
    if re.match(r'\d{4}\.\S+', raw):
        return raw
    raise ValueError(f"无法识别的 ACL Anthology ID 或 URL: {raw}")


def run(args):
    acl_id = normalize_acl_id(args.acl)
    arxiv_id = args.arxiv.strip() if args.arxiv else None
    code_url = args.code.strip() if args.code else None
    website_url = args.website.strip() if args.website else None

    print(f"\n=== 处理论文: {acl_id} ===")

    # 1. 获取 BibTeX
    bib = fetch_acl_bibtex(acl_id)
    if not bib:
        print("错误：无法获取 BibTeX，请检查 ACL Anthology ID 是否正确", file=sys.stderr)
        sys.exit(1)

    title = bib.get("title", "")
    author_str = bib.get("author", "")
    booktitle = bib.get("booktitle", "")
    year = bib.get("year", "")
    month = bib.get("month", "july")
    pages = bib.get("pages", "")
    acl_url = bib.get("url", f"https://aclanthology.org/{acl_id}/")
    acl_pdf_url = f"https://aclanthology.org/{acl_id}.pdf"
    doi = f"10.18653/v1/{acl_id}"

    if not title:
        print("错误：BibTeX 中未找到标题", file=sys.stderr)
        sys.exit(1)

    authors = parse_authors_bibtex(author_str)
    venue, track, pub_str = detect_venue(booktitle)

    print(f"  标题: {title}")
    print(f"  作者: {', '.join(authors)}")
    print(f"  发表: {pub_str}, {year}")
    if pages:
        print(f"  页码: {pages}")

    # 2. 获取摘要
    abstract = None
    if not args.no_abstract:
        abstract = fetch_acl_abstract(acl_id)
        if not abstract and arxiv_id:
            abstract = fetch_arxiv_abstract(arxiv_id)
        if abstract:
            print(f"  摘要: {abstract[:80]}...")
        else:
            print("  摘要: 未能自动获取（可手动添加）")

    # 3. 查找已有 arXiv 条目
    existing_dir = find_existing_arxiv_entry(title, arxiv_id)

    # 4. 确定目标目录
    if existing_dir and not args.no_merge:
        target_dir = existing_dir
        action = "更新（合并 arXiv 版本）"
    else:
        dir_name = make_dir_name(venue, year, title)
        target_dir = PUBLICATION_DIR / dir_name
        action = "新建" if not target_dir.exists() else "覆盖已有"

    print(f"  操作: {action}")
    print(f"  目录: {target_dir.relative_to(REPO_ROOT)}")

    # 5. 渲染 index.md
    content = render_index_md(
        title=title,
        authors=authors,
        venue=venue,
        track=track,
        pub_str=pub_str,
        year=year,
        month=month,
        pages=pages,
        doi=doi,
        acl_url=acl_url,
        acl_pdf_url=acl_pdf_url,
        arxiv_id=arxiv_id,
        code_url=code_url,
        website_url=website_url,
        abstract=abstract,
    )

    if args.dry_run:
        print("\n--- 预览 index.md ---")
        print(content)
        print("--- [dry-run，未写入文件] ---")
        return

    # 6. 写入文件
    target_dir.mkdir(parents=True, exist_ok=True)
    index_path = target_dir / "index.md"
    index_path.write_text(content, encoding="utf-8")
    print(f"\n  已写入: {index_path.relative_to(REPO_ROOT)}")
    print("  完成！")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="向 stair-team Hugo 主页添加或更新论文发表信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        示例:
          python scripts/add_publication.py 2026.acl-long.1471
          python scripts/add_publication.py https://aclanthology.org/2026.acl-long.1471/
          python scripts/add_publication.py 2026.acl-long.1471 --arxiv 2601.12906
          python scripts/add_publication.py 2026.acl-long.1471 --arxiv 2601.12906 --code https://github.com/org/repo
          python scripts/add_publication.py 2026.acl-long.1471 --dry-run
        """),
    )
    parser.add_argument(
        "acl",
        help="ACL Anthology ID (如 2026.acl-long.1471) 或完整 URL",
    )
    parser.add_argument(
        "--arxiv",
        metavar="ID",
        help="对应的 arXiv ID (如 2601.12906)，用于获取摘要或合并已有 arXiv 条目",
    )
    parser.add_argument(
        "--code",
        metavar="URL",
        help="代码仓库 URL",
    )
    parser.add_argument(
        "--website",
        metavar="URL",
        help="项目/演示页面 URL",
    )
    parser.add_argument(
        "--no-merge",
        action="store_true",
        help="即使存在已有 arXiv 条目，也强制新建目录",
    )
    parser.add_argument(
        "--no-abstract",
        action="store_true",
        help="跳过摘要获取",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅预览生成内容，不写入文件",
    )
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
