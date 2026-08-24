# Grasping Omron MOMA

This repository extends the [CollaborativeRoboticsLab/grasping](https://github.com/CollaborativeRoboticsLab/grasping) stack and uses it along with [CollaborativeRoboticsLab/mobile_manipulator](https://github.com/CollaborativeRoboticsLab/mobile_manipulator) stack to perform mobile manipulator based grasping for the Omron MOMA mobile manipulator with a TM12X arm and a soft two-finger gripper.

It holds robot specific launch and configuration in `grasping_omron_moma` while reusing the generic grasping runtime from `grasping_control` and the generic mobile-manipulator runtime from `mobile_manipulator_ros`.

![system overview](./docs/system.png)

## Getting Started

- [Devcontainer connection](./docs/ld250_tm12x_connection.md)
- [TF frames for gripper compatibility](./docs/ld250_tm12x_tf_frames.md)

## Starting the Camera

Use the following command to start the RealSense D435 camera.

```bash
source install/setup.bash
ros2 launch anygrasp_realsense d435.launch.py
```

## Bringing Up the Omron Grasping Stack

Bring up the Omron grasping stack on hardware:

```bash
source install/setup.bash
ros2 launch grasping_omron_moma ld250_tm12x_soft_two_fingers.launch.py
```

Run in demo mode:

```bash
source install/setup.bash
ros2 launch grasping_omron_moma ld250_tm12x_soft_two_fingers.launch.py use_demo:=true
```

Enable the mobile base and Nav2 when needed (manipulator is enabled by default):

```bash
source install/setup.bash
ros2 launch grasping_omron_moma ld250_tm12x_soft_two_fingers.launch.py use_base:=true use_nav2:=true
```

If you only want the raw arm, gripper, and MoveIt bringup without the grasping wrapper, you can still launch the MoveIt package directly:

```bash
source install/setup.bash
ros2 launch ld250_tm12x_soft_two_fingers_moveit_config hardware_with_moveit.launch.py
```

## Bringing Up Grasping Plus Task Feasibility

Bring up the Omron grasping stack together with the standalone mobile-manipulator task-feasibility runtime:

```bash
source install/setup.bash
ros2 launch grasping_omron_moma omron_task_feasibility_stack.launch.py
```

For demo mode:

```bash
source install/setup.bash
ros2 launch grasping_omron_moma omron_task_feasibility_stack.launch.py use_demo:=true
```

This launch starts:

- the Omron grasping bringup
- `motion_execution_node`
- `feasibility_service_node`
- the generic `mobile_manipulator_server` with Omron parameters

## Running the Simple Grasping Sequence

Run the simple named-pose grasping sequence after the motion stack is already running:

```bash
source install/setup.bash
ros2 launch grasping_omron_moma simple_grasping.launch.py
```

The default sequence is:

```text
[pose, pre_grasp] -> [pose, workspace_center] -> [gripper, open] -> [pose, grasp_pose] -> [gripper, close] -> [pose, post_grasp]
```

## Running Mobile-Manipulator Task Feasibility

If the grasp target may require moving the base before arm execution, start the Omron mobile-manipulator runtime:

```bash
source install/setup.bash
ros2 launch grasping_omron_moma task_feasibility.launch.py
```

To run the Omron test client against that runtime:

```bash
source install/setup.bash
ros2 launch grasping_omron_moma mobile_manipulator_control.launch.py
```

## Configuration

`grasping_omron_moma/config/motion_config.yaml` uses the current `motion_execution_node` schema from `grasping_control`.

Tune these fields before using the sequence on a real robot:

- `planning_joint_names`
- `poses_names`
- `poses_values.workspace_center`
- `poses_values.pre_grasp`
- `poses_values.grasp_pose`
- `poses_values.post_grasp`

`simple_grasping.launch.py` expects the named poses `pre_grasp`, `workspace_center`, `grasp_pose`, and `post_grasp` to exist in `motion_config.yaml`.

`grasping_omron_moma/config/crlab_table.yaml` defines the workspace objects and the planar workspace acceptance area used by `motion_execution_node`.

## Notes

- `grasping_omron_moma` is the standalone Omron-facing wrapper for both the grasping stack and the Omron mobile-manipulator runtime entry points.
- Generic motion execution, named-pose handling, joint-pose handling, and workspace validation live in `grasping_control`.
- Generic task-feasibility runtime and test-client logic live in `mobile_manipulator_ros` and `mobile_manipulator_control`.
- The default named poses in `motion_config.yaml` are placeholders and should be calibrated on the real robot.