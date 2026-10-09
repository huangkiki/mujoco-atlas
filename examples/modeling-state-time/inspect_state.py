"""Read native model/state fields. Source reviewed and syntax checked; not executed.

No mj_step call is made. Loading still invokes MuJoCo's compiler, which can run
internal consistency computations. Read docs/state-and-time.md before running.
"""

from pathlib import Path

import mujoco
import numpy as np


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(Path(__file__).with_name("frames.xml")))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)

    print("nq, nv, nu, nactuator:", model.nq, model.nv, model.nu, model.nactuator)
    for name in ("floating", "slide", "hinge", "ball"):
        joint = model.joint(name)
        print(name, "qpos address:", joint.qposadr, "qvel address:", joint.dofadr)
        print("configuration:", data.joint(name).qpos.copy())

    # The model has no sleeping, IPC, plugins, history or external controller.
    signature = mujoco.mjtState.mjSTATE_INTEGRATION
    saved = np.empty(mujoco.mj_stateSize(model, signature), dtype=data.qpos.dtype)
    mujoco.mj_getState(model, data, saved, signature)

    # Changing a configuration is not a control command or a dynamics step.
    data.joint("hinge").qpos[0] = 0.2
    mujoco.mj_forward(model, data)
    body_id = model.body("floating_box").id
    print("body origin:", data.xpos[body_id].copy())
    print("center of mass:", data.xipos[body_id].copy())
    print("site position:", data.site("box_tip").xpos.copy())

    # BODY asks for velocity at the center of mass; output order is angular,
    # then linear. flg_local=0 expresses both vectors along world axes.
    velocity = np.empty(6, dtype=data.qpos.dtype)
    mujoco.mj_objectVelocity(
        model, data, mujoco.mjtObj.mjOBJ_BODY, body_id, velocity, 0
    )
    print("world angular velocity, world CoM velocity:", velocity.copy())

    # Demonstrate a tangent-space displacement on a COPY, not a physics update.
    candidate = data.qpos.copy()
    tangent = np.zeros(model.nv, dtype=data.qvel.dtype)
    hinge_dof = int(model.jnt_dofadr[model.joint("hinge").id])
    tangent[hinge_dof] = 0.1  # rad/s; integratePos integrates given velocity only
    mujoco.mj_integratePos(model, candidate, tangent, 0.01)
    recovered = np.empty(model.nv, dtype=data.qvel.dtype)
    mujoco.mj_differentiatePos(model, recovered, 0.01, data.qpos, candidate)
    print("tangent-space velocity:", recovered)

    mujoco.mj_setState(model, data, saved, signature)
    mujoco.mj_forward(model, data)  # refresh derived fields after restoring inputs
    print("restored hinge:", data.joint("hinge").qpos.copy())

    key_id = model.key("reference").id
    mujoco.mj_resetDataKeyframe(model, data, key_id)
    mujoco.mj_forward(model, data)
    print("keyframe time:", data.time)


if __name__ == "__main__":
    main()
