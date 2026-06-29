---
title: 'Beyond Black-Box Interventions: Latent Probing for Faithful Retrieval-Augmented Generation'
authors:
- Linfeng Gao
- Qinggang Zhang
- Baolong Bi
- Bo Zeng
- Zheng Yuan
- Zerui Chen
- Zhimin Wei
- Shenghua Liu
- Linlong Xu
- Longyue Wang
- Weihua Luo
- Jinsong Su
date: '2026-07-01'
publishDate: '2026-06-29T00:00:00Z'
publication_types:
- paper-conference
publication: '*Findings of the Association for Computational Linguistics, ACL Findings, 2026, pages 29981–30000*'
doi: 10.18653/v1/2026.findings-acl.1499

abstract: "Retrieval-Augmented Generation (RAG) systems often fail to maintain contextual
  faithfulness, generating responses that conflict with the provided context or fail
  to fully leverage the provided evidence. In this paper, we move beyond black-box
  interventions to analyze the model's internal reasoning process. We discover that
  conflicting and aligned knowledge states are linearly separable in the model's latent
  space, and contextual noise systematically increases the entropy of these representations.
  Based on these findings, we propose ProbeRAG, a novel framework for faithful RAG
  that operates in three stages: (i) fine-grained knowledge pruning to filter irrelevant
  context, (ii) latent conflict probing to identify hard conflicts in the model's
  latent space, and (iii) conflict-aware attention to modulate attention heads toward
  faithful context integration. Extensive experiments demonstrate that ProbeRAG substantially
  improves both accuracy and contextual faithfulness."

featured: false

links:
- name: ACL Anthology
  url: https://aclanthology.org/2026.findings-acl.1499/
- name: arXiv
  url: https://arxiv.org/abs/2510.12460
- name: Code
  url: https://github.com/XMUDeepLIT/ProbeRAG

url_pdf: 'https://aclanthology.org/2026.findings-acl.1499.pdf'
url_code: 'https://github.com/XMUDeepLIT/ProbeRAG'
---
