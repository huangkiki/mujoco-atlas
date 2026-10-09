"""Bounded local XY IK for this two-hinge model; never executed in this phase.

Only scratch MjData is modified. This is kinematic fitting, without collision
checks, equality constraints, dynamics or an execution controller.
"""

from collections.abc import Sequence
from pathlib import Path

import mujoco
import numpy as np


def solve_position(
    model: mujoco.MjModel, target_xy: Sequence[float], initial_qpos: np.ndarray
) -> tuple[np.ndarray, float, bool]:
    """Return (candidate qpos, residual in metres, converged); no global guarantee."""
    if model.nq != 2 or model.nv != 2 or not np.all(
        model.jnt_type == mujoco.mjtJoint.mjJNT_HINGE
    ):
        raise ValueError("this teaching solver requires the two-hinge model")
    if initial_qpos.shape != (2,) or not np.isfinite(initial_qpos).all():
        raise ValueError("initial_qpos must be a finite two-vector")
    data = mujoco.MjData(model)
    data.qpos[:] = initial_qpos
    site_id = model.site("tip").id
    joints = [model.joint(name).id for name in ("shoulder", "elbow")]
    qadr = model.jnt_qposadr[joints]
    dofs = model.jnt_dofadr[joints]
    lower, upper = model.jnt_range[joints].T
    data.qpos[qadr] = np.clip(data.qpos[qadr], lower, upper)
    jacp = np.zeros((3, model.nv))
    length_scale = 0.5  # metres; makes task residual and Jacobian dimensionless here
    damping = 0.03
    tolerance = 1e-5  # metres, a teaching stop rule; not an experimentally qualified value
    target = np.asarray(target_xy, dtype=float)
    if target.shape != (2,) or not np.isfinite(target).all():
        raise ValueError("target_xy must be a finite two-vector")

    def residual() -> np.ndarray:
        # mj_jacSite consumes cdof/subtree_com; kinematics alone does not update them.
        mujoco.mj_kinematics(model, data)
        mujoco.mj_comPos(model, data)
        return target - data.site_xpos[site_id, :2]

    for _ in range(60):
        error = residual()
        error_norm = float(np.linalg.norm(error))
        if error_norm <= tolerance:
            return data.qpos.copy(), error_norm, True
        mujoco.mj_jacSite(model, data, jacp, None, site_id)
        jacobian = jacp[:2, dofs] / length_scale
        rhs = error / length_scale
        dq = jacobian.T @ np.linalg.solve(
            jacobian @ jacobian.T + damping**2 * np.eye(2), rhs
        )
        # Bound a local hinge displacement in radians; no physical time is advanced.
        dq *= min(1.0, 0.1 / max(float(np.linalg.norm(dq)), 1e-12))
        previous = data.qpos.copy()
        accepted = False
        for scale in (1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125):
            data.qpos[:] = previous
            tangent = np.zeros(model.nv)
            tangent[dofs] = scale * dq
            mujoco.mj_integratePos(model, data.qpos, tangent, 1.0)
            data.qpos[qadr] = np.clip(data.qpos[qadr], lower, upper)
            if np.linalg.norm(residual()) < error_norm:
                accepted = True
                break
        if not accepted:
            data.qpos[:] = previous
            break
    final_error = float(np.linalg.norm(residual()))
    return data.qpos.copy(), final_error, final_error <= tolerance


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(Path(__file__).with_name("two_link.xml")))
    seed = model.qpos0.copy()
    seed[model.jnt_qposadr[model.joint("shoulder").id]] = 0.2
    seed[model.jnt_qposadr[model.joint("elbow").id]] = -0.4
    qpos, residual, converged = solve_position(model, [0.35, 0.1], seed)
    print("candidate:", qpos, "residual (m):", residual, "converged:", converged)


if __name__ == "__main__":
    main()
