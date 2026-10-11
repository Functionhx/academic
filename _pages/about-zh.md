---
permalink: /zh/
title: ""
excerpt: ""
lang: zh
author_profile: true
---

<span class='anchor' id='about-me'></span>

我是樊宇琛（Yuchen Fan），[北京理工大学](https://www.bit.edu.cn/)机器人工程专业本科生。我的工作横跨算法、软件与硬件，希望把机器人研究做成可靠的系统，尤其重视真机部署与结果可复现。

**研究兴趣：** 具身智能、自主系统、三维场景智能（3D Gaussian Splatting、SLAM）与机器人学习。

<span class='anchor' id='news'></span>

# 🔥 动态

- _2026.09_：我的论文 *When Does KV Cache Compression Pay?*（KVLedger）被 GPC 2026 录用为 Regular Paper。
- _2026.07_：SinD 2.0 在 [arXiv](https://arxiv.org/abs/2607.16943) 发布。这是一个面向信号灯路口 SOTIF 安全验证的多城市无人机数据集。

<span class='anchor' id='publications'></span>

# 📝 论文

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">GPC 2026</div><img src='{{ "/images/kvledger-teaser.jpg" | relative_url }}' alt="压缩是否划算取决于链路：同一 GPU 上永不划算，PCIe 上的分界点是 1.06–2.08 MB，双 GPU P2P 上是 23–46 MB" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

[When Does KV Cache Compression Pay? A Quality- and Cost-Aware Runtime Framework for Cloud LLM Serving](https://functionhx.github.io/kv-compression-pays/)

**Yuchen Fan**

_International Conference on Green, Pervasive, and Cloud Computing (GPC)_, 2026，Springer LNCS，待出版 · [**项目主页**](https://functionhx.github.io/kv-compression-pays/) · [**审稿意见与回应**]({{ site.links.blog }}blog/2026/kvledger-gpc2026-reviews/)

- KVLedger 把编解码、元数据、传输和接收端开销都记进账里，按链路、按模型判断分离式 LLM 推理中 KV cache 压缩是否划算。
</div>
</div>

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">arXiv 2026</div><img src='{{ "/images/sind2-teaser.jpg" | relative_url }}' alt="SinD 2.0 基于 3DGS 的视觉仿真渲染出的自车视角画面" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

[SinD 2.0: A Multi-City UAV Dataset with Semantic Risk Annotations for SOTIF-Oriented Safety Validation at Signalized Intersections](https://arxiv.org/abs/2607.16943)

Yunwei Li, Shengjie Fu, Chunrong Chen, Chengxiang Zhao, **Yuchen Fan**, Mingyu Zhu, Yanchao Xu, Jiahui Xu, Anran Wang, Huanan Wang, Yuxin Zhang, Lan Yang, Chuzhao Li, Jie Ji, Yi He, Abhijit Sarkar, Akash Sonth, Hong Wang, Jun Li

_arXiv preprint_, 2026 · [**arXiv**](https://arxiv.org/abs/2607.16943) · [**PDF**](https://arxiv.org/pdf/2607.16943) · [**Dataset**](https://github.com/SOTIF-AVLab/SinD)

- 我的贡献：数据标注，以及基于 3DGS 的视觉仿真扩展（论文 VI-G 节）。
</div>
</div>

<span class='anchor' id='research'></span>

# 🔬 研究

- [**三维场景智能**]({{ site.links.blog }}research/3d-scene-intelligence/)。面向导航、视觉定位与可编辑场景生成的三维表示。

<span class='anchor' id='education'></span>

# 📖 教育

- _2023 – 2027_，[北京理工大学](https://www.bit.edu.cn/)自动化学院，机器人工程专业本科生。
