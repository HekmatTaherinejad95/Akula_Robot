from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command

import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
# from launch.actions import ExecuteProcess
import launch_ros.actions

def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                get_package_share_directory('velodyne_driver'),
                '/launch/velodyne_driver_node-VLP16-launch.py'
            ])
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                get_package_share_directory('velodyne_pointcloud'),
                '/launch/velodyne_convert_node-VLP16-launch.py'
            ])
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'robot_description': Command([
                    'xacro',
                    ' ',
                   get_package_share_directory('AkulaPackage') + '/model/akula.urdf'
                ])
            }]
        ),

        Node(
            package='wheeltec_n100_imu',
            executable='imu_node',
            name='imu_node'
        ),

        launch.actions.ExecuteProcess( 
         cmd=['ros2', 'run', 'atgm336h5n3x', 'nmea_node', '--dev', '/dev/ttyUSB0'], 
         output='screen'),

        launch.actions.ExecuteProcess( 
         cmd=['ros2', 'launch', 'localization', 'loc.launch.py'], 
         output='screen'),


        Node(
            package='BaslerROS2',
            executable='BaslerNode',
            name='Basler'
        ),
        Node(
            package='akula_package',
            executable='AkulaEncoderNode',
            name='AkulaEncoders'
        ),
        #Node(
        #    package='AkulaPackage',
        #    executable='AkulaImuNode',
        #    name='AkulaIMU'
        #)
    ])
