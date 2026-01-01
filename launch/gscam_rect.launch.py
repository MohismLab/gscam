# This file is dependent on isaac_ros_image_proc in isaac_ros docker 
from launch import LaunchDescription
from launch_ros.actions import Node, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

# Supported video formats and resolutions:
# [1]: 'YUYV' (YUYV 4:2:2)
#     Size: Discrete 1280x720
#         Interval: Discrete 0.111s (9.000 fps)
#     Size: Discrete 1920x1080
#         Interval: Discrete 0.167s (6.000 fps)
#     Size: Discrete 1024x768
#         Interval: Discrete 0.167s (6.000 fps)
#     Size: Discrete 640x480
#         Interval: Discrete 0.033s (30.000 fps)
#     Size: Discrete 800x600
#         Interval: Discrete 0.050s (20.000 fps)
#     Size: Discrete 1280x1024
#         Interval: Discrete 0.167s (6.000 fps)
#     Size: Discrete 320x240
#         Interval: Discrete 0.033s (30.000 fps)

def generate_launch_description():
    return LaunchDescription([
        # Composable Node Container for gscam and image_proc
        ComposableNodeContainer(
            name='gscam_image_proc_container',
            namespace='',
            package='rclcpp_components',
            executable='component_container_mt',  # Multi-threaded container
            composable_node_descriptions=[
                # gscam node as a composable node
                ComposableNode(
                    package='gscam',
                    plugin='gscam::GSCam',  
                    name='gscam_node',
                    remappings=[
                        ('/camera/image_raw', '/camera/image'),
                        # ('/camera/camera_info', 'camera_info'),
                    ],
                    parameters=[{
                        'framerate': 30,
                        'camera_name': 'default',
                        'camera_info_url': 'package://gscam/cfg/1.ini',
                        #'gscam_config': 'v4l2src device=/dev/video0 ! video/x-raw,width=640,height=480 ! nvvidconv ! videoconvert',
                        #'gscam_config': 'v4l2src device=/dev/video0 ! image/jpeg,width=640,height=480 ! jpegdec ! nvvidconv ! videoconvert',
                        'gscam_config': 'v4l2src device=/dev/video0 ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! nvvidconv ! videoconvert',
                        'frame_id': '/camera',
                        'sync_sink': True,
                        'reopen_on_eof': True,
                    }],
                    extra_arguments=[{'use_intra_process_comms': True}],
                ),
                # image_proc node as a composable node
                ComposableNode(
                    package='image_proc',
                    plugin='image_proc::RectifyNode',
                    name='mono_rectify_node',
                    namespace='camera',
                    extra_arguments=[{'use_intra_process_comms': True}],
                    # remappings=[
                    #     ('image', 'image_mono'),
                    #     ('image_rect', 'image_rect_mono'),
                    # ],
                    parameters=[{
                        'approximate_sync': True  # Allow approximate synchronization
                    }],
                )
            ],
            output='screen',
        )
    ])
