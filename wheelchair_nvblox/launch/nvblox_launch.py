# Copyright 2025 Lihan Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LoadComposableNodes
from launch_ros.descriptions import ComposableNode, ParameterFile
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    # Get the launch directory
    bringup_dir = get_package_share_directory("wheelchair_nvblox")

    namespace = LaunchConfiguration("namespace")
    use_sim_time = LaunchConfiguration("use_sim_time")
    params_file = LaunchConfiguration("params_file")
    container_name = LaunchConfiguration("container_name")
    container_name_full = (namespace, "/", container_name)

    # Create our own temporary YAML files that include substitutions
    param_substitutions = {"use_sim_time": use_sim_time}

    configured_params = ParameterFile(
        RewrittenYaml(
            source_file=params_file,
            root_key=namespace,
            param_rewrites=param_substitutions,
            convert_types=True,
        ),
        allow_substs=True,
    )

    stdout_linebuf_envvar = SetEnvironmentVariable(
        "RCUTILS_LOGGING_BUFFERED_STREAM", "1"
    )

    colorized_output_envvar = SetEnvironmentVariable("RCUTILS_COLORIZED_OUTPUT", "1")

    declare_namespace_cmd = DeclareLaunchArgument(
        "namespace", default_value="", description="Top-level namespace"
    )

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
        description="Use simulation (Gazebo) clock if true",
    )

    declare_params_file_cmd = DeclareLaunchArgument(
        "params_file",
        default_value=os.path.join(bringup_dir, "params", "reality", "realsense.yaml"),
        description="Full path to the ROS2 parameters file to use for all launched nodes",
    )

    declare_container_name_cmd = DeclareLaunchArgument(
        "container_name",
        default_value="vslam_container",
        description="the name of container that nodes will load in if use composition",
    )

    load_composable_nodes = LoadComposableNodes(
        target_container=container_name_full,
        composable_node_descriptions=[
            ComposableNode(
                name="realsense_splitter_node",
                package="realsense_splitter",
                plugin="nvblox::RealsenseSplitterNode",
                parameters=[configured_params],
                remappings=[
                    ("input/infra_1", "/left_d435i/infra1/image"),
                    ("input/infra_1_metadata", "/left_d435i/infra1/metadata"),
                    ("input/infra_2", "/left_d435i/infra2/image"),
                    ("input/infra_2_metadata", "/left_d435i/infra2/metadata"),
                    ("input/depth", "/left_d435i/depth/image"),
                    ("input/depth_metadata", "/left_d435i/depth/metadata"),
                    ("input/pointcloud", "/left_d435i/depth/color/points"),
                    ("input/pointcloud_metadata", "/left_d435i/depth/metadata"),
                ],
            ),
            ComposableNode(
                package="nvblox_ros",
                plugin="nvblox::NvbloxNode",
                name="nvblox_node",
                parameters=[configured_params],
                remappings=[
                    ("camera_0/color/camera_info", "left_d435i/color/camera_info"),
                    ("camera_0/color/image", "left_d435i/color/image"),
                    ("camera_0/depth/camera_info", "left_d435i/depth/camera_info"),
                    ("camera_0/depth/image", "realsense_splitter_node/output/depth"),
                    # ("camera_0/depth/image", "left_d435i/depth/image"),
                    ("pointcloud", "livox/lidar"),
                ],
            ),
        ],
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    # Set environment variables
    ld.add_action(stdout_linebuf_envvar)
    ld.add_action(colorized_output_envvar)

    # Declare the launch options
    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_params_file_cmd)
    ld.add_action(declare_container_name_cmd)

    # Add the actions to launch all of the localiztion nodes
    ld.add_action(load_composable_nodes)

    return ld
