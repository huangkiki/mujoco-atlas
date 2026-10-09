# MuJoCo Atlas

Understand MuJoCo through native APIs, physics concepts and versioned source code.

[中文](README.md) · [Series home](https://github.com/huangkiki/sim-atlas) · [Introductory guide](docs/guide.md) · [Curriculum](docs/curriculum.md) · [Source map](docs/source-map.md) · [Versions](docs/versions.md) · [Roadmap](docs/roadmap.md) · [Project tracker](https://github.com/users/huangkiki/projects/2)

Part of **[Sim Atlas](https://github.com/huangkiki/sim-atlas)**, an independent community learning series with two complete planned tracks: applications (modeling, control, robotics, sensing and data) and principles/source (dynamics, contact, solvers, integration and extensions).

The introductory guide, pinned source map and E1 chapters are available in Chinese: [modeling and frames](docs/modeling-and-frames.md) and [state and time](docs/state-and-time.md). E1 covers A1/A2 and the foundations of B0/B4, including coordinate/inertia conventions, state ownership, snapshots, sampling phases and integration semantics. E2 now covers [actuation and control](docs/actuation-and-control.md), [robotics and kinematics](docs/robotics-and-kinematics.md), and [task interfaces](docs/task-interfaces.md), including multi-input actuator blocks, force clamping, bounded local IK and observation-driven task transitions. The full course is in development.

[Original examples](examples/modeling-state-time/README.md) have only passed static Python/XML checks; they were not compiled or executed by MuJoCo. [Validation and source discrepancies](docs/validation/e1.md) separate source review from runtime evidence. This phase prioritizes understanding engine subsystems. Minimal snippets support explanation and are explicitly marked when unexecuted. No new simulation campaigns, benchmarks, training or scoring are included; later experimental material will reuse [DexLab](https://github.com/huangkiki/Dexlab) with its original version and workload boundaries.

E2 examples received syntax/source review only: no model compilation, IK execution or grasping run was performed. [E2 validation](docs/validation/e2.md) records the exact scope and next-stage dependencies.

E3 now covers [dynamics and the step pipeline](docs/dynamics-and-pipeline.md), [contact models and material mixing](docs/contact-models.md), [solvers and integration](docs/solvers-and-integration.md), and [force observations](docs/force-observations.md). This completes the A4/B0–B5 core lessons, with version-specific convergence, warmstarts, discrete metrics, contact frames and sampling contracts. [Original examples](examples/contact-solvers/README.md) and [E3 validation](docs/validation/e3.md) are source/static only; no native compilation, forward/step, collision or numerical experiment was run. Detailed flex/IPC internals and backend extensions remain E6.

[Pinned upstream source](https://github.com/google-deepmind/mujoco/tree/9ea3cdfcae93bf2cc4dc0e1a1627c5a39a1e06e5) · [Attribution](THIRD_PARTY.md)
