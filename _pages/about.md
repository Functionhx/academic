---
permalink: /
title: ""
excerpt: ""
lang: en
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

<span class='anchor' id='about-me'></span>

I am Yuchen Fan (樊宇琛), a Robotics Engineering undergraduate at [Beijing Institute of Technology](https://english.bit.edu.cn/). I work across algorithms, software, and hardware to turn robotics research into reliable systems, with an emphasis on real-robot deployment and reproducible results.

**Research interests:** embodied AI, autonomous systems, 3D scene intelligence (3D Gaussian Splatting, SLAM), and robot learning.

<span class='anchor' id='news'></span>

# 🔥 News

- _2026.07_: SinD 2.0, a multi-city UAV dataset for SOTIF-oriented safety validation at signalized intersections, is released on [arXiv](https://arxiv.org/abs/2607.16943).

<span class='anchor' id='publications'></span>

# 📝 Publications

<div class='paper-box'><div class='paper-box-image'><div><div class="badge">arXiv 2026</div><img src='{{ "/images/sind2-teaser.jpg" | relative_url }}' alt="Egocentric views rendered by the SinD 2.0 3DGS-based visual simulation pipeline" width="100%"></div></div>
<div class='paper-box-text' markdown="1">

[SinD 2.0: A Multi-City UAV Dataset with Semantic Risk Annotations for SOTIF-Oriented Safety Validation at Signalized Intersections](https://arxiv.org/abs/2607.16943)

Yunwei Li, Shengjie Fu, Chunrong Chen, Chengxiang Zhao, **Yuchen Fan**, Mingyu Zhu, Yanchao Xu, Jiahui Xu, Anran Wang, Huanan Wang, Yuxin Zhang, Lan Yang, Chuzhao Li, Jie Ji, Yi He, Abhijit Sarkar, Akash Sonth, Hong Wang, Jun Li

_arXiv preprint_, 2026 · [**arXiv**](https://arxiv.org/abs/2607.16943) · [**PDF**](https://arxiv.org/pdf/2607.16943) · [**Dataset**](https://github.com/SOTIF-AVLab/SinD)

- My contribution: data annotation and the 3DGS-based visual simulation extension (Sec. VI-G).
</div>
</div>

<span class='anchor' id='research'></span>

# 🔬 Research

- **3DGS-based instance image goal navigation** (under review). Online 3D Gaussian Splatting mapping coupled with active exploration so a robot can find a specific object instance from a reference image.
- **[Batch-LIO](https://github.com/Functionhx/Batch-LIO)**. A batch-wise extension of Point-LIO that reproduces the batch-update idea of Point-LIWO: ~1 ms time-window grouping, in-batch motion de-skew, and batched EKF updates with OpenMP, kept A/B-comparable with Point-LIO. [Engineering details →]({{ site.links.blog_en }}projects/batch-lio/)
- **[RoboAccel](https://github.com/Functionhx/RoboAccel)**. An end-to-end stack that deploys a trained RL policy to a Zynq-7000 FPGA and an STM32H723 MCU with bit-exact fixed-point verification; for a wheel-legged robot balance controller, FPGA pure inference is 14.4× faster than the same policy on Cortex-M7.
- **3D Scene Intelligence**. 3D representations for navigation, visual localization, and editable scene generation. [Engineering details →]({{ site.links.blog_en }}research/3d-scene-intelligence/)
- **Formula Student Driverless**. Autonomous-system integration and track engineering. [Engineering details →]({{ site.links.blog_en }}projects/formula-student-driverless/)
