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

- _2026.07_：SinD 2.0 在 [arXiv](https://arxiv.org/abs/2607.16943) 发布。这是一个面向信号灯路口 SOTIF 安全验证的多城市无人机数据集。

<span class='anchor' id='publications'></span>

# 📝 论文

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

- **基于 3DGS 的实例图像目标导航**（在投）。将在线 3D Gaussian Splatting 建图与主动探索结合，让机器人根据一张参考图像找到场景中的特定物体实例。
- **[Batch-LIO](https://github.com/Functionhx/Batch-LIO)**。Point-LIO 的批处理扩展，复现 Point-LIWO 的批量更新思路：约 1 ms 时间窗分组、批内运动去畸变、结合 OpenMP 的批量 EKF 更新，并与 Point-LIO 保持可 A/B 对比。[工程细节 →]({{ site.links.blog_zh }}projects/batch-lio/)
- **[RoboAccel](https://github.com/Functionhx/RoboAccel)**。把训练好的强化学习策略端到端部署到 Zynq-7000 FPGA 与 STM32H723 MCU，并做逐位一致的定点验证；在轮腿机器人平衡控制器上，FPGA 纯推理比同一策略在 Cortex-M7 上快 14.4 倍。
- **三维场景智能**。面向导航、视觉定位与可编辑场景生成的三维表示。[工程细节 →]({{ site.links.blog_zh }}research/3d-scene-intelligence/)
- **学生方程式无人驾驶**。自主系统集成与赛道工程。[工程细节 →]({{ site.links.blog_zh }}projects/formula-student-driverless/)
