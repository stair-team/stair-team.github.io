# stair-team 主页维护脚本

## add_publication.py — 添加/更新论文发表信息

从 **ACL Anthology** 自动获取论文元信息，生成或更新 Hugo 网站中的 publication 条目。

### 功能

- 自动从 ACL Anthology 获取 BibTeX（标题、作者、页码、DOI 等）
- 自动抓取论文摘要（优先从 ACL Anthology，其次 arXiv）
- 智能检测并合并已有的 arXiv 预印本条目（不产生重复）
- 支持 ACL、EMNLP、NAACL、EACL、COLING、ICLR、NeurIPS、ICML、AAAI、IJCAI、KDD、WWW 等主流会议
- `--dry-run` 模式可预览生成内容而不写入文件

### 依赖

仅使用 Python 标准库，无需额外安装。

### 用法

```bash
# 基础用法（仅提供 ACL Anthology ID）
python3 scripts/add_publication.py 2026.acl-long.1471

# 提供完整 URL 也可以
python3 scripts/add_publication.py https://aclanthology.org/2026.acl-long.1471/

# 同时提供 arXiv ID：用于获取摘要，并自动合并已有 arXiv 条目
python3 scripts/add_publication.py 2026.acl-long.1471 --arxiv 2601.12906

# 添加代码仓库和项目页面链接
python3 scripts/add_publication.py 2026.acl-long.1471 \
    --arxiv 2601.12906 \
    --code https://github.com/org/repo \
    --website https://project.page

# 预览生成内容，不写入文件
python3 scripts/add_publication.py 2026.acl-long.1471 --dry-run

# 强制新建目录（忽略已有 arXiv 条目）
python3 scripts/add_publication.py 2026.acl-long.1471 --no-merge
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `acl` | ACL Anthology ID（如 `2026.acl-long.1471`）或完整 URL（必填） |
| `--arxiv ID` | 对应的 arXiv 论文 ID，用于获取摘要或自动合并已有 arXiv 条目 |
| `--code URL` | 代码仓库 URL |
| `--website URL` | 项目/演示页面 URL |
| `--no-merge` | 强制新建目录，不合并已有 arXiv 条目 |
| `--no-abstract` | 跳过摘要自动获取 |
| `--dry-run` | 预览模式，只打印生成内容，不写入文件 |

### 工作流

1. 在 ACL Anthology 找到论文页面，复制 ID（如 `2026.acl-long.1471`）
2. 运行脚本（可先加 `--dry-run` 预览）
3. 脚本自动判断是**新建**还是**更新**已有 arXiv 条目
4. 检查生成的 `content/publication/.../index.md` 文件
5. `git add && git commit && git push`

### ACL Anthology ID 格式说明

```
2026.acl-long.1471        → ACL 2026 Main (Long Papers)
2026.acl-short.0123       → ACL 2026 Main (Short Papers)
2026.findings-acl.1240    → ACL 2026 Findings
2025.emnlp-main.698       → EMNLP 2025 Main
2025.findings-emnlp.456   → EMNLP 2025 Findings
2025.naacl-long.321       → NAACL 2025 Main
```
