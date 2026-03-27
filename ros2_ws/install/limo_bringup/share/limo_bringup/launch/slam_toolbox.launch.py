#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    
    ld = LaunchDescription()

    slam_toolbox_dir = os.path.join(
            get_package_share_directory('slam_toolbox'),
            'launch')

    slam_toolbox_config_dir = os.path.join(
        get_package_share_directory('limo_bringup'),
        'param',
        'slam_toolbox_custom.yaml')
        #'slam_toolbox_online_async.yaml')


    slam_toolbox_launch = IncludeLaunchDescription(
        launch_description_source=os.path.join(slam_toolbox_dir, 'online_async_launch.py'),
        launch_arguments={
            'slam_params_file': slam_toolbox_config_dir
        }.items()
    )

    rviz_config_dir = os.path.join(
        get_package_share_directory('limo_bringup'),
        'rviz',
        'mapping.rviz')

    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir])

    ld.add_action(slam_toolbox_launch)
    ld.add_action(rviz2)

    return ld
