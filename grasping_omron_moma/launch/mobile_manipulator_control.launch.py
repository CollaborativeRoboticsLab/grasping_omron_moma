from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    grasping_omron_moma_share = get_package_share_directory('grasping_omron_moma')
    mobile_manipulator_control_share = get_package_share_directory('mobile_manipulator_control')

    generic_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(Path(mobile_manipulator_control_share) / 'launch' / 'mobile_manipulator_control.launch.py')
        ),
        launch_arguments={
            'config_file': LaunchConfiguration('config_file'),
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                'config_file',
                default_value=str(Path(grasping_omron_moma_share) / 'config' / 'mobile_manipulator_control.yaml'),
            ),
            generic_launch,
        ]
    )