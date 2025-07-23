# wheelchair_nvblox

- Run VSLAM with realsense d435i

  ```bash
  ros2 launch wheelchair_nvblox bringup_launch.py
  ```

- Run VSLAM with simulation

  ```bash
  ros2 launch wheelchair_nvblox bringup_launch.py params_file:=src/wheelchair_nvblox/params/simulation/realsense.yaml use_sim_time:=True slam:=False world:=simulation_20250707
  ```

- Run VSLAM with rosbag

  ```bash
  ros2 launch wheelchair_nvblox bringup_launch.py use_sim_time:=True slam:=False world:=fnii_20250711
  ```

- Play rosbag realsense_20250711_140223 in FNii

  ```bash
  ros2 bag play realsense_20250711_140223 --clock
  ```
