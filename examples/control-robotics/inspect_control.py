"""Source-reviewed, syntax-checked only; no MuJoCo execution was performed.

This prints native block addresses and one forward force evaluation, not a
trajectory. The XML compiler can perform internal dynamics consistency checks.
"""

from pathlib import Path

import mujoco


def main() -> None:
    model = mujoco.MjModel.from_xml_path(str(Path(__file__).with_name("two_link.xml")))
    data = mujoco.MjData(model)
    print("actuators, scalar inputs, force outputs:", model.nactuator, model.nu, model.nout)

    for name in ("shoulder_servo", "elbow_motor"):
        actuator_id = model.actuator(name).id
        input_start = int(model.actuator_ctrladr[actuator_id])
        input_count = int(model.actuator_ctrlnum[actuator_id])
        output_start = int(model.actuator_outadr[actuator_id])
        output_count = int(model.actuator_outnum[actuator_id])
        print(name, "input:", input_start, input_count, "output:", output_start, output_count)

    servo_id = model.actuator("shoulder_servo").id
    servo_start = int(model.actuator_ctrladr[servo_id])
    data.ctrl[servo_start:servo_start + 2] = [0.1, 0.0]  # rad, rad/s; gear=1
    motor_id = model.actuator("elbow_motor").id
    motor_start = int(model.actuator_ctrladr[motor_id])
    data.ctrl[motor_start] = 10.0  # deliberately outside this model's motor ctrlrange
    requested = data.ctrl.copy()
    mujoco.mj_forward(model, data)
    print("requested controls remain stored:", requested, data.ctrl.copy())
    print("actuator output forces:", data.actuator_force.copy())
    print("joint-space actuator forces after joint clamping:", data.qfrc_actuator.copy())
    print("sample phase: forward at time", data.time)


if __name__ == "__main__":
    main()
