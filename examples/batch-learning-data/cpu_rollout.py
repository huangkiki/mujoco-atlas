"""Read native CPU rollout contracts; source/AST reviewed, never executed here.

Running this script would compile a model and advance physics. It is not a
training environment, benchmark or complete checkpoint implementation.
"""
from pathlib import Path

import mujoco
from mujoco import rollout
import numpy as np


def main():
    model = mujoco.MjModel.from_xml_path(str(Path(__file__).with_name("slider.xml")))
    batch, horizon, workers = 4, 8, 2
    spec = mujoco.mjtState.mjSTATE_FULLPHYSICS
    state_width = mujoco.mj_stateSize(model, spec)
    initial = np.empty((batch, state_width), dtype=mujoco.MJTNUM_DTYPE)
    seed_data = mujoco.MjData(model)
    joint_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, "slide")
    qpos_address = model.jnt_qposadr[joint_id]
    for index, position in enumerate((-0.03, -0.01, 0.01, 0.03)):
        mujoco.mj_resetData(model, seed_data)
        seed_data.qpos[qpos_address] = position
        mujoco.mj_getState(model, seed_data, initial[index], spec)

    # One distinct writable workspace per worker; model remains read-only.
    data = [mujoco.MjData(model) for _ in range(workers)]
    control = np.zeros((batch, horizon, model.nu), dtype=mujoco.MJTNUM_DTYPE)
    control[:, :, 0] = np.asarray((-0.5, 0.0, 0.25, 0.5))[:, None]
    warmstart = np.zeros((batch, model.nv), dtype=mujoco.MJTNUM_DTYPE)
    with rollout.Rollout(nthread=workers) as pool:
        state, sensors = pool.rollout(
            model,
            data,
            initial,
            control,
            initial_warmstart=warmstart,
        )

    # FULLPHYSICS starts with time. These checks are necessary, not sufficient:
    # a warning on the final step need not create any repeated output frame.
    expected_time = initial[:, :1] + model.opt.timestep * np.arange(1, horizon + 1)
    if not np.isfinite(state).all() or not np.isfinite(sensors).all():
        raise RuntimeError("Non-finite batch output")
    if not np.allclose(state[:, :, 0], expected_time, rtol=1e-5, atol=1e-8):
        raise RuntimeError("Unexpected time progression; inspect warning/fill behavior")

    print({
        "state_shape": state.shape,
        "sensor_shape": sensors.shape,
        "state_mask": int(spec),
        "dtype": str(state.dtype),
        "state_phase": "after mj_step integration",
        "sensor_phase": "values left by mj_step, not refreshed after integration",
        "validity": "shape/finite/time checks do not certify all warnings or physics",
    })


if __name__ == "__main__":
    main()
