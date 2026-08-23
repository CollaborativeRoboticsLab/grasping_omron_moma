from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
	grasping_control_share = get_package_share_directory('grasping_control')
	grasping_omron_moma_share = get_package_share_directory('grasping_omron_moma')

	default_sequence = '[[pose, pre_grasp], [pose, workspace_center], [gripper, open], [pose, grasp_pose], [gripper, close], [pose, post_grasp]]'

	simple_grasping = IncludeLaunchDescription(
		PythonLaunchDescriptionSource(
			str(Path(grasping_control_share) / 'launch' / 'simple_grasping.launch.py')
		),
		launch_arguments={
			'arm_action_name': '/move_arm_to_named_pose',
			'gripper_action_name': '/gripper_command',
			'sequence': LaunchConfiguration('sequence'),
			'open_position': LaunchConfiguration('open_position'),
			'open_max_effort': LaunchConfiguration('open_max_effort'),
			'close_position': LaunchConfiguration('close_position'),
			'close_max_effort': LaunchConfiguration('close_max_effort'),
			'server_timeout_sec': LaunchConfiguration('server_timeout_sec'),
			'result_timeout_sec': LaunchConfiguration('result_timeout_sec'),
		}.items(),
	)

	return LaunchDescription(
		[
			DeclareLaunchArgument(
				'motion_config_file',
				default_value=str(Path(grasping_omron_moma_share) / 'config' / 'motion_config.yaml'),
			),
			DeclareLaunchArgument('sequence', default_value=default_sequence),
			DeclareLaunchArgument('open_position', default_value='0.09'),
			DeclareLaunchArgument('open_max_effort', default_value='0.0'),
			DeclareLaunchArgument('close_position', default_value='0.0'),
			DeclareLaunchArgument('close_max_effort', default_value='5.0'),
			DeclareLaunchArgument('server_timeout_sec', default_value='10.0'),
			DeclareLaunchArgument('result_timeout_sec', default_value='120.0'),
			simple_grasping,
		]
	)