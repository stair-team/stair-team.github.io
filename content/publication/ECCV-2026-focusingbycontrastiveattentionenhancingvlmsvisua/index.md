---
title: "Focusing by Contrastive Attention: Enhancing VLMs' Visual Reasoning"
authors:
- Yuyao Ge
- Shenghua Liu
- Yiwei Wang
- Lingrui Mei
- Baolong Bi
- Xuanshan Zhou
- Jiayu Yao
- Jiafeng Guo
- Xueqi Cheng
date: '2026-10-01'
publishDate: '2026-06-29T00:00:00Z'
publication_types:
- paper-conference
publication: '*Proc. of the European Conference on Computer Vision, ECCV, 2026*'

abstract: "Vision-Language Models (VLMs) have demonstrated remarkable success across
  diverse visual tasks, yet their performance degrades in complex visual environments.
  While existing enhancement approaches require additional training, rely on external
  segmentation tools, or operate at coarse-grained levels, they overlook the innate
  ability within VLMs. We investigate VLMs' attention patterns and discover that:
  (1) visual complexity strongly correlates with attention entropy, negatively impacting
  reasoning performance; (2) attention progressively refines from global scanning
  in shallow layers to focused convergence in deeper layers. (3) Theoretically, we
  prove that the contrast of attention maps between general queries and task-specific
  queries enables the decomposition of visual signal into semantic signals and visual
  noise components. Building on these insights, we propose CARVE (Contrastive Attention
  Refinement for Visual Enhancement), a training-free method that extracts task-relevant
  visual signals through attention contrasting at the pixel level. Extensive experiments
  demonstrate that CARVE consistently enhances performance, achieving up to 75% improvement
  on open-source models."

featured: true

links:
- name: arXiv
  url: https://arxiv.org/abs/2509.06461
- name: Website
  url: https://geyuyao.com/publication/ge2025focusing/

url_pdf: 'https://arxiv.org/pdf/2509.06461'
---
