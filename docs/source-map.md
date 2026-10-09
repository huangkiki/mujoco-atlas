# mujoco-atlas 固定版本源码入口

阅读基线：`9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5`。以下入口已核对官方 Git 树与文件内容身份；不是全仓审查或运行验收记录。

本阶段先理解引擎架构、建模、步进、控制、接触/求解、传感器/渲染、性能与扩展。独立实验、基准、训练和评分暂不开展，后续复用 DexLab。

| 源码文件 | 阅读目的 |
|---|---|
| [include/mujoco/mjmodel.h](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/include/mujoco/mjmodel.h) | 核对对象职责、数据布局、参数与版本约定 |
| [include/mujoco/mjdata.h](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/include/mujoco/mjdata.h) | 核对对象职责、数据布局、参数与版本约定 |
| [src/engine/engine_forward.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_forward.c) | 追踪构建、步进、数据更新与生命周期 |
| [src/engine/engine_solver.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_solver.c) | 识别算法、输入状态、配置与限制 |
| [src/engine/engine_collision_driver.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_collision_driver.c) | 区分接触几何、接触律与数值近似 |
| [src/engine/engine_core_constraint.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_core_constraint.c) | 识别算法、输入状态、配置与限制 |
| [doc/programming/simulation.rst](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/doc/programming/simulation.rst) | 核对对象职责、数据布局、参数与版本约定 |
| [doc/programming/modeledit.rst](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/doc/programming/modeledit.rst) | 核对对象职责、数据布局、参数与版本约定 |
| [doc/modeling.rst](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/doc/modeling.rst) | 核对对象职责、数据布局、参数与版本约定 |
| [doc/computation/index.rst](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/doc/computation/index.rst) | 核对对象职责、数据布局、参数与版本约定 |
| [python/mujoco/renderer.py](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/python/mujoco/renderer.py) | 区分传感数据、可视化与物理状态 |
