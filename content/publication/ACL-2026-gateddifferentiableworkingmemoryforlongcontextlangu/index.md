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
publishDate: '2026-06-29T00:00:00Z'
publication_types:
- paper-conference
publication: '*Proc. of the Association for Computational Linguistics, ACL Main, 2026, pages 31885–31913*'
doi: 10.18653/v1/2026.acl-long.1471

abstract: "Long contexts break transformers: attention scores dilute across thousands
  of tokens, critical information gets lost in the middle, and the model cannot adapt
  to novel patterns at inference time. We reframe test-time adaptation as a budget-constrained
  memory consolidation problem and propose GDWM (Gated Differentiable Working Memory),
  a framework that introduces a Write Controller to gate the memory consolidation
  process. Our controller estimates Contextual Utility—an information-theoretic measure
  quantifying how much each region depends on long-range context—and allocates gradient
  steps accordingly, subject to a coverage constraint that ensures global representation.
  Experiments on ZeroSCROLLS and LongBench v2 benchmarks demonstrate that GDWM achieves
  comparable or superior performance with 4× fewer gradient steps compared to uniform
  baselines, establishing a new efficiency-performance Pareto frontier for test-time
  adaptation."

featured: true

links:
- name: ACL Anthology
  url: https://aclanthology.org/2026.acl-long.1471/
- name: arXiv
  url: https://arxiv.org/abs/2601.12906

url_pdf: 'https://aclanthology.org/2026.acl-long.1471.pdf'
---
