---
title: 'Gated Differentiable Working Memory for Long-Context Language Modeling'
authors:
- Lingrui Mei
- Shenghua Liu
- Yiwei Wang
- Yuyao Ge
- Baolong Bi
- Jiayu Yao
- Jun Wan
- Ziling Yin
- Jiafeng Guo
- Xueqi Cheng
date: '2026-07-01'
publishDate: '2026-07-01T00:00:00Z'
publication_types:
- paper-conference
publication: '*Proceedings of the 64th Annual Meeting of the Association for Computational
  Linguistics (Volume 1: Long Papers), ACL 2026, pages 31885–31913*'
doi: 10.18653/v1/2026.acl-long.1471

abstract: "Long contexts break transformers: attention scores dilute across thousands
  of tokens, critical information gets lost in the middle, and the model struggles
  to adapt to novel patterns at inference time. Test-time adaptation addresses this
  by maintaining a form of working memory—transient parameters updated on the current
  context—but existing approaches employ uniform write policies that waste computation
  on low-value regions and suffer from high gradient variance across semantically
  heterogeneous contexts. In this work, we reframe test-time adaptation as a budget-constrained
  memory consolidation problem, asking: given limited computational budget, which
  parts of the context should be consolidated into working memory? We propose GDWM
  (Gated Differentiable Working Memory), a framework that introduces a Write Controller
  to gate the memory consolidation process. Our controller estimates Contextual Utility—an
  information-theoretic measure quantifying how much each region depends on long-range
  context—and allocates gradient steps accordingly, subject to a coverage constraint
  that ensures global representation. Experiments on ZeroSCROLLS and LongBench v2
  benchmarks demonstrate that GDWM achieves comparable or superior performance with
  4× fewer gradient steps compared to uniform baselines, establishing a new efficiency-performance
  Pareto frontier for test-time adaptation."

featured: false

links:
- name: ACL Anthology
  url: https://aclanthology.org/2026.acl-long.1471/
- name: arXiv
  url: https://arxiv.org/abs/2601.12906

url_pdf: 'https://aclanthology.org/2026.acl-long.1471.pdf'

image:
  caption: ''
  focal_point: ''
  placement: 2
  preview_only: false
---
