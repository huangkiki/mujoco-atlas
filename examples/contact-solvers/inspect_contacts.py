"""MuJoCo 3.15.0 native field-reading example; not executed for this course.

Calling this file would compile a model and call mj_forward once. The compiler
may itself perform test calculations. It is not a collision or force benchmark.
"""
from pathlib import Path

import mujoco
import numpy as np


def main() -> None:
    if mujoco.mj_versionString() != "3.15.0":
        raise RuntimeError("This example targets the reviewed MuJoCo 3.15.0 API")
    model = mujoco.MjModel.from_xml_path(str(Path(__file__).with_name("plane_spheres.xml")))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    solve_time = float(data.time)
    print("query time; no interval elapsed:", solve_time)
    print("integrator, solver, cone:", model.opt.integrator, model.opt.solver, model.opt.cone)
    print("h, iteration cap, tolerance:", model.opt.timestep, model.opt.iterations, model.opt.tolerance)
    print("detected contacts, scalar constraint rows:", data.ncon, data.nefc)

    for index in range(data.ncon):
        contact = data.contact[index]
        geom_ids = tuple(int(item) for item in contact.geom)
        print("contact:", index, "geoms:", geom_ids, "dist:", float(contact.dist),
              "dim:", int(contact.dim), "exclude:", int(contact.exclude),
              "efc_address:", int(contact.efc_address))
        if any(geom_id < 0 for geom_id in geom_ids):
            print("flex contact: outside this geom-only example")
            continue
        if contact.efc_address < 0:
            print("no constraint rows; do not index efc_force with -1")
            continue
        local_wrench = np.zeros(6)
        mujoco.mj_contactForce(model, data, index, local_wrench)
        contact_axes = np.asarray(contact.frame).reshape(3, 3).copy()
        force_world = contact_axes.T @ local_wrench[:3]
        torque_at_contact = contact_axes.T @ local_wrench[3:]
        body_id = int(model.geom_bodyid[geom_ids[1]])
        lever = np.asarray(contact.pos) - data.xipos[body_id]
        torque_at_com = torque_at_contact + np.cross(lever, force_world)
        print("net local force:torque:", local_wrench.copy())
        print("geom[1] world force and CoM torque:", force_world, torque_at_com)

    # Bare inertia, not the effective metric of the discrete integrator.
    mass = np.empty((model.nv, model.nv))
    mujoco.mj_fullM(model, data, mass)
    print("dense inertia shape:", mass.shape)
    if data.nefc:
        generalized = np.empty(model.nv)
        mujoco.mj_mulJacTVec(model, data, generalized, data.efc_force)
        # For this ordinary, non-adhesive, non-IPC model only. This is a reading
        # diagnostic, not a pass/fail claim or an independent physics score.
        print("J.T @ efc_force:", generalized.copy())
        print("qfrc_constraint:", data.qfrc_constraint.copy())


if __name__ == "__main__":
    main()
