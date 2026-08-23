from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    grasping_omron_moma_share = get_package_share_directory('grasping_omron_moma')
    mobile_manipulator_ros_share = get_package_share_directory('mobile_manipulator_ros')

    generic_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(Path(mobile_manipulator_ros_share) / 'launch' / 'task_feasibility.launch.py')
        ),
        launch_arguments={
            'config_file': LaunchConfiguration('config_file'),
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'config_file',
                default_value=str(Path(grasping_omron_moma_share) / 'config' / 'task_feasibility.yaml'),
            ),
            generic_launch,
        ]
    )