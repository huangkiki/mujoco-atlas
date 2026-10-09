"""Inspect native flex ownership and derived coordinates; never executed here.

If run later, this compiles MJCF and calls mj_forward. The compiler itself may
perform test calculations. There is no mj_step, renderer or experiment loop.
"""
from pathlib import Path

import mujoco


def main():
    path = Path(__file__).with_name("flex_patch.xml")
    model = mujoco.MjModel.from_xml_path(str(path))
    data = mujoco.MjData(model)
    flex_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_FLEX, "patch")
    if flex_id < 0:
        raise ValueError("Expected flex named patch")

    # Refresh derived positions. MjData allocation is not a full forward pass.
    mujoco.mj_forward(model, data)
    start = int(model.flex_vertadr[flex_id])
    stop = start + int(model.flex_vertnum[flex_id])
    dimension = int(model.flex_dim[flex_id])
    element_start = int(model.flex_elemdataadr[flex_id])
    element_count = int(model.flex_elemnum[flex_id])
    element_stop = element_start + element_count * (dimension + 1)
    connectivity = model.flex_elem[element_start:element_stop].reshape(
        element_count, dimension + 1
    ).copy()

    print({
        "flex_dimension": dimension,
        "qpos_width": model.nq,
        "velocity_width": model.nv,
        "vertex_body_ids": model.flex_vertbodyid[start:stop].copy(),
        "world_attached_vertices": [
            local_id for local_id, body_id in enumerate(
                model.flex_vertbodyid[start:stop]
            ) if body_id == 0
        ],
        "element_local_vertex_ids": connectivity,
        "vertex_world_positions_m": data.flexvert_xpos[start:stop].copy(),
        "phase": "after mj_forward, before any explicit mj_step",
    })


if __name__ == "__main__":
    main()
