#!/bin/zsh

# Record realsense rosbag in real world 
source install/setup.zsh

ros2 bag record -o spin_$(date +%Y%m%d_%H%M%S) \
  /clock \
  /tf \
  /tf_static \
  /camera/infra1/image_rect_raw \
  /camera/infra1/camera_info \
  /camera/infra2/image_rect_raw \
  /camera/infra2/camera_info \
  /camera/imu \
  --compression-mode file --compression-format zstd -d 30
