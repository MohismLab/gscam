from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gscam',
            executable='gscam_node',
            name='gscam',
            output='screen',
            remappings=[
               ('/camera/image_raw', 'image_raw'),
               ('/camera/camera_info', 'camera_info'),
           ],
            parameters=[{
                'framerate': 30,
                'camera_name': 'default',
                'camera_info_url': 'package://gscam/cfg/1.ini',
                #'camera_info_url': 'package://gscam/cfg/fyheo.ini',
                'gscam_config': 'v4l2src device=/dev/video0 ! video/x-raw,width=640,height=480 ! nvvidconv ! videoconvert',
                'gscam_config': 'v4l2src device=/dev/video0 ! image/jpeg,width=1920,height=1080 ! jpegdec ! nvvidconv ! videoconvert',
                'frame_id': '/camera',
                #'image_encoding': 'jpeg',
                'sync_sink': True,
                'reopen_on_eof': True,
            }]
        )
    ])

