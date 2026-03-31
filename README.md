# LIMO ROS2 Humble Docker Environment
 
・DockerによるLIMO用ROS2環境
・再現性・共有性を目的とする
 
## 構成
・Dockerfile
・docker-compose
・limo_ros2（submodule予定）



## 
time NTP

xhost



○要修正箇所
LIMO ProだとURATポートが違う 
→ 親のlimo_start.launch.py, 子のlimo_base.launch.pyともに、port_nameを'ttyTHS1'から'ttyTHS0'に変えておく

LiDAR用のframe_idが異なる
→ 親のlimo_start.launch.pyから呼び出される、子のopen_ydlidar_launch.pyにおいて、frame_idが、laser_linkでなく
    laser_frameと定義されている。そのため、bindしているTminiPro用のparamを記述したyamlにおいて、frame_idをlaser_frameと定義しておく

slamtoolboxのyaml
minimum_distance_penalty: 0.05  (0.5 -> 0.05)
max_laser_range: 25.0  ( 8.0 -> 25.0)



navigation.yamlの指定mapの中国語.pgmみたいになっているのをmapにするべき、もっというと保存先はros2_ws/mapsをバインドするべきだし、もっというとその状態で更に引数で指定する形にしておくのが望ましい。
root@master:~/ros2_ws# ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/limo_ros2/limo_bringup/maps/mymap --ros-args -p map_subscribe_transient_local:=true






ros2 launch limo_bringup navigation2.launch.py \
map:=/root/ros2_ws/src/limo_ros2/limo_bringup/maps/mymap.yaml



need orbbec-v1(OpenNI) 

