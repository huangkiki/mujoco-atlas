"""Read one prepared state; source/syntax reviewed, never executed in this course stage."""

from pathlib import Path

import mujoco


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(Path(__file__).with_name("observations.xml")))
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)
    sample_time = float(data.time)

    # This is the time of the prepared state; none of these sensors uses history.
    for name in ("angular_velocity", "specific_force", "imu_in_camera", "imu_pixel"):
        print(name, sample_time, data.sensor(name).data.copy())

    camera_id = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_CAMERA, "top")
    width, height = map(int, model.cam_resolution[camera_id])
    # Each pixel stores dist(1), point(3), depth(1), in exactly that order.
    rays = data.sensor("rays").data.copy().reshape(height, width, 5)
    hit = rays[..., 0] >= 0
    print("rays", rays.shape, "valid hits", int(hit.sum()))

    # Use a provider configured before Python imports MuJoCo. Creation needs GL.
    with mujoco.Renderer(model, height=height, width=width) as renderer:
        renderer.update_scene(data, camera="top")
        rgb = renderer.render().copy()
        renderer.enable_depth_rendering()
        axial_depth = renderer.render().copy()
        renderer.enable_segmentation_rendering()
        object_labels = renderer.render().copy()

    print("RGB", sample_time, rgb.shape, rgb.dtype)
    print("depth", sample_time, axial_depth.shape, axial_depth.dtype)
    print("object labels", sample_time, object_labels.shape, object_labels.dtype)
    # Deliberately no claim that ray hits and visual pixels coincide.


if __name__ == "__main__":
    main()
