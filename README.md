# wheelchair

## 1. Overview

Autonomous wheelchair navigation using ROS2 and NVIDIA Isaac ROS. It integrates various components, including visual SLAM, nvblox, and Gazebo simulation environments.

> [!NOTE]
> Full navigation stacks NOT Done.

## 2. Quick Start

### 2.1 Setup Environment

- Ubuntu 22.04
- ROS: [Humble](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)
- Ignition: [Fortress](https://gazebosim.org/docs/fortress/install_ubuntu/)
- CUDA version: [12.6](https://developer.nvidia.com/cuda-12-6-3-download-archive)
- Driver Version: 560.35.05

  ```bash
  wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
  sudo dpkg -i cuda-keyring_1.0-1_all.deb
  sudo apt update

  sudo apt install nvidia-driver-560
  ```

- Setup Nvidia Isaac Repos

  ```bash
  # Download and add NVIDIA Isaac ROS key
  wget -qO - https://isaac.download.nvidia.com/isaac-ros/repos.key | sudo gpg --dearmor -o /usr/share/keyrings/isaac-ros-archive-keyring.gpg

  # Add NVIDIA Isaac ROS repository
  echo "deb [signed-by=/usr/share/keyrings/isaac-ros-archive-keyring.gpg] https://isaac.download.nvidia.com/isaac-ros/release-3 jammy release-3.0" | sudo tee /etc/apt/sources.list.d/isaac-ros.list

  # Update package list
  sudo apt-get update
  ```

  ```bash
  # Add NVIDIA Jetson public key
  sudo apt-key adv --fetch-key https://repo.download.nvidia.com/jetson/jetson-ota-public.asc

  # Add Jetson repository
  sudo add-apt-repository "deb http://repo.download.nvidia.com/jetson/x86_64/$(lsb_release -cs) r36.3 main"

  # Update package list and install VPI libraries
  sudo apt-get update
  sudo apt-get install -y libnvvpi3 vpi3-dev
  ```

  ```bash
  git clone -b release-3.2 https://github.com/NVIDIA-ISAAC-ROS/isaac_ros_common.git ~/isaac_ros_ws/src/isaac_ros_common
  ```

  ```bash
  cd ~/isaac_ros_ws/src/isaac_ros_common/docker/rosdep/
  sudo cp extra_rosdeps.yaml /etc/ros/rosdep/sources.list.d/nvidia-isaac.yaml
  echo "yaml file:///etc/ros/rosdep/sources.list.d/nvidia-isaac.yaml" | sudo tee /etc/ros/rosdep/sources.list.d/00-nvidia-isaac.list
  sudo sed -i 's|gbpdistro https://raw.githubusercontent.com/ros/rosdistro/master/releases/fuerte.yaml fuerte||g' /etc/ros/rosdep/sources.list.d/20-default.list

  rosdep update
  ```

### 2.2 Create Workspace

```bash
sudo pip install vcstool2
pip install xmacro
```

```bash
git clone https://github.com/LihanChen2004/wheelchair.git ~/ros_ws/src
```

```bash
cd ~/ros_ws/src
vcs import --recursive . < dependencies.repos
```

Option: Download rosbag and pre-built map

```bash
cd ~/ros_ws
```

```bash
# Download and extract rosbag
gdown https://drive.google.com/uc?id=11Z99dv6SHaO31cP_r8wA1J1Gzs1HRQMf -O rosbag.zip
unzip rosbag.zip -d .

# Download and extract pre-built map
gdown https://drive.google.com/uc?id=1S1yT6gdU4U1EEtWuu1oL3lJjR9lqjD5_ -O map.zip
unzip map.zip -d src/wheelchair_nvblox/maps
```

### 2.3 Build

```bash
cd ~/ros_ws
```

```bash
rosdep install -r --from-paths src --ignore-src --rosdistro $ROS_DISTRO -y
```

```bash
colcon build --symlink-install
```

### 2.4 Running

#### 2.4.1 Play rosbag

- Launch nvblox and vslam

  ```bash
  ros2 launch wheelchair_nvblox bringup_launch.py use_sim_time:=True slam:=False world:=fnii_20250711
  ```

- Play rosbag realsense_20250711_140223

  ```bash
  ros2 bag play realsense_20250711_140223 --clock
  ```

#### 2.4.2 realsense d435i camera

  ```bash
  ros2 launch wheelchair_nvblox bringup_launch.py
  ```

#### 2.4.3 Simulation

  > [!NOTE]
  > Currently, `isaac_ros_nvblox` is not supported in simulation, only `isaac_ros_visual_slam` is supported.

  ```bash
  ros2 launch wheelchair_simulator bringup_sim_launch.py
  ```

  ```bash
  ros2 launch wheelchair_slam bringup_launch.py params_file:=src/wheelchair_slam/params/simulation/realsense.yaml use_sim_time:=True slam:=True
  ```
