import os

import launch
from ament_index_python import get_package_share_directory
from launch.actions import SetEnvironmentVariable
from launch_ros.actions import ComposableNodeContainer, Node
from launch_ros.descriptions import ComposableNode


def generate_launch_description():
    stdout_linebuf_envvar = SetEnvironmentVariable(
        "RCUTILS_LOGGING_BUFFERED_STREAM", "1"
    )

    colorized_output_envvar = SetEnvironmentVariable("RCUTILS_COLORIZED_OUTPUT", "1")

    visual_slam_node = ComposableNode(
        package="isaac_ros_visual_slam",
        plugin="nvidia::isaac_ros::visual_slam::VisualSlamNode",
        name="visual_slam_node",
        parameters=[
            {
                "use_sim_time": True,
                "enable_image_denoising": False,
                "rectified_images": True,
                "enable_imu_fusion": True,
                "gyro_noise_density": 0.000244,
                "gyro_random_walk": 0.000019393,
                "accel_noise_density": 0.001862,
                "accel_random_walk": 0.003,
                "calibration_frequency": 200.0,
                "image_jitter_threshold_ms": 40.00,
                "base_frame": "camera_link",
                "imu_frame": "camera_gyro_optical_frame",
                "enable_slam_visualization": True,
                "enable_landmarks_view": True,
                "enable_observations_view": True,
                "camera_optical_frames": [
                    "camera_infra1_optical_frame",
                    "camera_infra2_optical_frame",
                ],
            }
        ],
        remappings=[
            ("visual_slam/image_0", "camera/infra1/image_rect_raw"),
            ("visual_slam/camera_info_0", "camera/infra1/camera_info"),
            ("visual_slam/image_1", "camera/infra2/image_rect_raw"),
            ("visual_slam/camera_info_1", "camera/infra2/camera_info"),
            ("visual_slam/imu", "camera/imu"),
        ],
    )

    visual_slam_launch_container = ComposableNodeContainer(
        name="visual_slam_launch_container",
        namespace="",
        package="rclcpp_components",
        executable="component_container",
        composable_node_descriptions=[visual_slam_node],
        output="screen",
    )

    start_rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        arguments=[
            "-d",
            os.path.join(
                get_package_share_directory("wheelchair_slam"),
                "rviz",
                "realsense.rviz",
            ),
        ],
    )

    # Create the launch description and populate
    ld = launch.LaunchDescription()

    # Set environment variables
    ld.add_action(stdout_linebuf_envvar)
    ld.add_action(colorized_output_envvar)

    # Add the actions to launch all of the navigation nodes
    # ld.add_action(realsense_camera_node)
    ld.add_action(visual_slam_launch_container)
    ld.add_action(start_rviz)

    return ld

