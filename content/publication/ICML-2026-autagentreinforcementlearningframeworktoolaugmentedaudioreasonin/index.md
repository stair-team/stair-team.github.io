---
title: 'AuTAgent: A Reinforcement Learning Framework for Tool-Augmented Audio Reasoning'
authors:
- Siqian Tong
- Xuan Li
- Yiwei Wang
- Baolong Bi
- Yujun Cai
- Shenghua Liu
- Yuchen He
- Chengpeng Hao
date: '2026-07-01'
publishDate: '2026-07-01T00:00:00Z'
publication_types:
- paper-conference
publication: '*Proc. of the International Conference on Machine Learning, ICML 2026*'

abstract: "Large Audio Language Models (LALMs) excel at perception but struggle with
  complex reasoning requiring precise acoustic measurements. While external tools
  can extract fine-grained features like exact tempo or pitch, effective integration
  remains challenging: naively using all tools causes information overload, while
  prompt-based selection fails to assess context-dependent utility. To address this,
  we propose AuTAgent (Audio Tool Agent), a reinforcement learning framework that
  learns when and which tools to invoke. By employing a sparse-feedback training strategy
  with a novel Differential Reward mechanism, the agent learns to filter out irrelevant
  tools and invokes external assistance only when it yields a net performance gain
  over the base model. Experimental results confirm that AuTAgent complements the
  representation bottleneck of LALMs by providing verifiable acoustic evidence. It
  improves accuracy by 4.20% / 6.20% and 9.80% / 8.00% for open-source and closed-source
  backbones on the MMAU Test-mini and the MMAR benchmarks, respectively. In addition,
  further experiments demonstrate exceptional transferability. We highlight the complementary
  role of external tools in augmenting audio model reasoning."

featured: false

links:
- name: arXiv
  url: https://arxiv.org/abs/2602.13685
- name: Website
  url: https://tongsiqian.github.io/AuTAgent

url_pdf: 'https://arxiv.org/pdf/2602.13685'

image:
  caption: ''
  focal_point: ''
  placement: 2
  preview_only: false
---
