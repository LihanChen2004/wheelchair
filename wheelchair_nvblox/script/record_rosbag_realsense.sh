#!/bin/zsh

# Record realsense rosbag in real world 
source install/setup.zsh

ros2 bag record -o realsense_$(date +%Y%m%d_%H%M%S) \
  /tf_static \
  /left_d435i/infra1/camera_info \
  /left_d435i/infra1/metadata \
  /left_d435i/infra1/image \
  /left_d435i/infra2/camera_info \
  /left_d435i/infra2/metadata \
  /left_d435i/infra2/image \
  /left_d435i/depth/camera_info \
  /left_d435i/depth/metadata \
  /left_d435i/depth/image \
  /left_d435i/color/camera_info \
  /left_d435i/color/image \
  /left_d435i/imu
