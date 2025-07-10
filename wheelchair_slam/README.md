# wheelchair_slam

## Dependencies

- CUDA version: 12.6

- Driver Version: 560.35.05

  ```Shell
  wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
  sudo dpkg -i cuda-keyring_1.0-1_all.deb
  sudo apt update

  sudo apt install nvidia-driver-560
  ```

```bash
rosdep install -r --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y
```

## Build

```bash
colcon build --symlink-install
```

## Quick Start

- Run VSLAM with realsense d435i

  ```bash
  ros2 launch wheelchair_slam bringup_launch.py
  ```

- Run VSLAM with simulation

  ```bash
  ros2 launch wheelchair_slam bringup_launch.py params_file:=src/wheelchair_slam/params/simulation/realsense.yaml use_sim_time:=True slam:=False world:=simulation_20250707
  ```

- Run VSLAM with rosbag

  ```bash
  ros2 launch wheelchair_slam bringup_launch.py use_sim_time:=True slam:=False world:=fnii_20250702
  ```

- Play rosbag realsense_20250702_135435 in FNii

  ```bash
  ros2 bag play realsense_20250702_135435 \
    --remap /camera/infra1/camera_info:=/left_d435i/infra1/camera_info \
    /camera/infra1/image_rect_raw:=/left_d435i/infra1/image \
    /camera/infra2/camera_info:=/left_d435i/infra2/camera_info \
    /camera/infra2/image_rect_raw:=/left_d435i/infra2/image \
    /camera/imu:=/left_d435i/imu
  ```
