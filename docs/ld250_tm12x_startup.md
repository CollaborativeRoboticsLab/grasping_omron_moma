# LD250 TM12X Manipulator

## Installation

We have configured the devcontainer to install the drivers required by the TM robots during the build process.
    
If you are setting this up yourself (outside the devcontainer) and using a Techman Robot Manipulator, follow the official instructions [here](https://github.com/CollaborativeRoboticsLab/tm2_ros2)

## Calibration

We use an `ld250_tm12x` mobile manipulator with the TM12X arm mounted on the LD250 base and the soft two-finger gripper attached to the tool side.

## Start the Manipulator MoveIt Stack

Use the following command to start the combined LD250 + TM12X + gripper MoveIt stack:

```bash
source install/setup.bash
ros2 launch ld250_tm12x_soft_two_fingers_moveit_config hardware_with_moveit.launch.py tm_robot_ip:=<robot_controller_ip>
```

The hardware launch starts the TM driver, MoveIt, and soft two-finger gripper action server on `/gripper_command`. Do not start `gripper_ros gripper_soft_two_fingers.launch.py` separately with this stack unless you intentionally want an independent gripper-only session.

The launch file defines these primary arguments:

- `tm_robot_ip:=<robot_controller_ip>`
- `tm_use_simulation:=false`
- `no_logging:=false`
- `launch_servo:=false`

Enable Servo if you want jogging through the forward position controller:

```bash
source install/setup.bash
ros2 launch ld250_tm12x_soft_two_fingers_moveit_config hardware_with_moveit.launch.py \
	tm_robot_ip:=<robot_controller_ip> \
	launch_servo:=true
```

For demo mode without hardware, use:

```bash
source install/setup.bash
ros2 launch ld250_tm12x_soft_two_fingers_moveit_config demo.launch.py
```

## Notes

If controller activation fails during physical bringup, check the active controllers in `/controller_manager` and switch the required combined arm controller explicitly.

```bash
source install/setup.bash
ros2 control list_controllers
ros2 service call /controller_manager/switch_controller controller_manager_msgs/srv/SwitchController "{activate_controllers: ['tmr_arm_with_base_controller'], deactivate_controllers: ['forward_position_controller'], strictness: 1, activate_asap: true, timeout: {sec: 5, nanosec: 0}}"
```