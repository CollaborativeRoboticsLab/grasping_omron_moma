from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    grasping_omron_moma_share = get_package_share_directory('grasping_omron_moma')

    grasping_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(Path(grasping_omron_moma_share) / 'launch' / 'ld250_tm12x_soft_two_fingers.launch.py')
        ),
        launch_arguments={
            'use_demo': LaunchConfiguration('use_demo'),
            'motion_config_file': LaunchConfiguration('motion_config_file'),
            'workspace_file': LaunchConfiguration('workspace_file'),
            'use_base': LaunchConfiguration('use_base'),
            'use_nav2': LaunchConfiguration('use_nav2'),
            'tm_robot_ip': LaunchConfiguration('tm_robot_ip'),
            'tm_use_simulation': LaunchConfiguration('tm_use_simulation'),
            'no_logging': LaunchConfiguration('no_logging'),
            'launch_servo': LaunchConfiguration('launch_servo'),
        }.items(),
    )

    task_feasibility = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(Path(grasping_omron_moma_share) / 'launch' / 'task_feasibility.launch.py')
        ),
        launch_arguments={
            'config_file': LaunchConfiguration('task_feasibility_config_file'),
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument('use_demo', default_value='false'),
            DeclareLaunchArgument(
                'motion_config_file',
                default_value=str(Path(grasping_omron_moma_share) / 'config' / 'motion_config.yaml'),
            ),
            DeclareLaunchArgument(
                'workspace_file',
                default_value=str(Path(grasping_omron_moma_share) / 'config' / 'crlab_table.yaml'),
            ),
            DeclareLaunchArgument(
                'task_feasibility_config_file',
                default_value=str(Path(grasping_omron_moma_share) / 'config' / 'task_feasibility.yaml'),
            ),
            DeclareLaunchArgument('use_base', default_value='false'),
            DeclareLaunchArgument('use_nav2', default_value='false'),
            DeclareLaunchArgument('tm_robot_ip', default_value=''),
            DeclareLaunchArgument('tm_use_simulation', default_value='false'),
            DeclareLaunchArgument('no_logging', default_value='false'),
            DeclareLaunchArgument('launch_servo', default_value='false'),
            grasping_bringup,
            task_feasibility,
        ]
    )