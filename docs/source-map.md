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
| [python/mujoco/renderer.py](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/python/mujoco/renderer.py) | E4：旧路径仅兼容转发；实际 classic 实现在下方新模块 |
| [doc/XMLreference.rst](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/doc/XMLreference.rst) | E1：编译选项、局部坐标、inertial、freejoint align、mesh/URDF 与资产语义 |
| [doc/python.rst](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/doc/python.rst) | E1：原生绑定的内存视图、命名访问、GIL、nstep 与重编译生命周期 |
| [include/mujoco/mjtype.h](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/include/mujoco/mjtype.h) | E1：mjtState 的 3.15.0 准确枚举与 history/integration 组合 |
| [include/mujoco/mujoco.h](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/include/mujoco/mujoco.h) | E1：state API 与 objectVelocity rot:lin 的公开契约 |
| [src/engine/engine_support.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_support.c) | E1：state mask 复制、配置积分/差分与四元数处理 |
| [src/engine/engine_core_smooth.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_core_smooth.c) | E1：父子 pose、FK、free/ball 速度轴与空间运动基 |
| [src/engine/engine_core_util.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_core_util.c) | E1：BODY/XBODY 的速度参考点、局部/世界轴变换 |
| [src/engine/engine_io.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_io.c) | E1：reset、keyframe、history 与四元数中性 ctrl |
| [src/engine/engine_util_spatial.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_util_spatial.c) | E1：右乘局部旋转增量的四元数积分 |

E1 的结论、行锚、文档冲突与静态验收见[验证记录](validation/e1.md)。文件身份核对与专题逐段阅读分开记录，未读部分不据此宣称已掌握。

## E2 驱动、机器人与任务接口

| 源码文件 | 阅读目的 |
|---|---|
| [src/user/user_api.cc](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/user/user_api.cc) | E2：motor/position/velocity/PID/orientation shortcut 写入的 gain/bias/dynamics 参数 |
| [src/user/user_objects.cc](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/user/user_objects.cc) | E2：joint 限位、SO3/PID 兼容性、输入宽度与逐输入控制范围编译 |
| [src/xml/xml_native_reader.cc](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/xml/xml_native_reader.cc) | E2：XML actuator 类型到原生 mjs_setTo* 的解析路径 |
| [src/engine/engine_callback.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_callback.c) | E2：进程级全局 mjcb_control 的所有权与重置 |
| [src/engine/engine_inverse.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_inverse.c) | E2：逆动力学所需总外加广义力，区分 IK 与控制分配 |

E2 同时深入读取既有 `engine_forward.c` 的 actuation、`engine_core_smooth.c` 的 transmission、`engine_core_util.c` 的 Jacobian 与 `XMLreference.rst` 的原生契约，详见[验证记录](validation/e2.md)。

## E3 动力学、接触、求解与力观测

| 源码文件 | 阅读目的 |
|---|---|
| [src/engine/engine_init.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_init.c) | E3：默认 option/solref/solimp 与报告运行配置的区别 |
| [src/engine/engine_passive.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_passive.c) | E3：geom adhesion 的被动力与净接触力账本 |
| [src/engine/engine_sensor.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_sensor.c) | E3：touch 正法向/区域条件与 force/torque 的 site 变换；完整传感接口已在 E4 展开 |
| [src/engine/engine_derivative.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_derivative.c) | E3：discrete 有效 metric、stiffness shift、coupling 限制与独立 free-body 陀螺项 |
| [src/engine/engine_derivative_fd.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_derivative_fd.c) | E3：有限差分状态维度、恢复与 RK4/history/sleep 限制 |
| [src/engine/engine_island.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_island.c) | E3：树/约束及 discrete tendon/flex metric 耦合的岛建图 |

E3 同时逐段核对既有 forward/collision/constraint/solver/core_smooth/core_util 与数据头文件，覆盖 CRB/RNE、几何与材料混合、primal/dual、停止条件、warmstart、积分与 contactForce。来源冲突、实际检查和扩展范围见[验证记录](validation/e3.md)。

## E4 传感、相机、查询与渲染

| 源码文件 | 阅读目的 |
|---|---|
| [doc/programming/visualization.rst](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/doc/programming/visualization.rst) | E4：mjv/mjr 分层、相机、scene、OpenGL context 和 GPU 资源契约 |
| [python/mujoco/__init__.py](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/python/mujoco/__init__.py) | E4：公开 Renderer 的实际导入以及 ImportError 边界 |
| [python/mujoco/rendering/classic/renderer.py](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/python/mujoco/rendering/classic/renderer.py) | E4：真实 classic RGB/depth/segmentation shape、深度反变换、资源生命周期 |
| [python/mujoco/rendering/classic/gl_context.py](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/python/mujoco/rendering/classic/gl_context.py) | E4：导入时 MUJOCO_GL 选择器；headless 与 context 禁用的区别 |
| [python/mujoco/rendering/filament/renderer.py](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/python/mujoco/rendering/filament/renderer.py) | E4：独立 Context/scene/target/view、CPU buffer、同步读回契约 |
| [python/mujoco/viewer.py](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/python/mujoco/viewer.py) | E4：launch/passive、macOS 主线程、handle 的 sync/lock/upload/close |
| [simulate/simulate.cc](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/simulate/simulate.cc) | E4：passive sync 的显示副本、INTEGRATION+forward 和 GUI 输入回传 |
| [src/engine/engine_ray.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_ray.c) | E4：射线过滤、非单位方向参数、mesh/primitive/SDF 分派 |
| [src/engine/engine_util_misc.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_util_misc.c) | E4：像素中心/正交射线、history 边界钳位与插值 |
| [src/engine/engine_vis_init.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_vis_init.c) | E4：可视化 scene 的容量与资源分配/释放 |
| [src/engine/engine_vis_visualize.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_vis_visualize.c) | E4：camera frustum、scene maxgeom 溢出、updateScene 只消费派生缓存 |
| [src/render/classic/render_gl3.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/render/classic/render_gl3.c) | E4：classic 视口宽高比与透视/正交投影 |
| [src/engine/engine_collision_sdf.c](https://github.com/google-deepmind/mujoco/blob/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5/src/engine/engine_collision_sdf.c) | E4：tactile 依赖的形状距离分派及不支持类型 |

E4 同时深入读取既有 engine_sensor 的内置/用户/plugin 分派、contact/tactile 和 history，user_api/user_objects 的维度/阶段/内参编译，以及 support/forward 的查询和历史读写。文档/实现差异与真实静态验收见[验证记录](validation/e4.md)。只下载但未作为结论依据的文件没有冒充已完成专题。
