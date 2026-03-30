# =========================================================
# TechShare LIMO Pro
# ROS 2 Humble Docker Image
# =========================================================
#
# ・ workspace(ros2_ws) は bind で外部管理
# ・ limo_pro_ros2 / astra_camera は submodule を bind
# ・ GPU / CUDA 依存は含めない
#
# =========================================================

FROM ros:humble


# ---------------------------------------------------------
# 作業ディレクトリ
# ---------------------------------------------------------
WORKDIR /root/ros2_ws
ENV DEBIAN_FRONTEND=noninteractive


# ---------------------------------------------------------
# 基本ツール + ROS2フルセット
# desktop + slam-toolbox + navigation2 を明示追加
# ---------------------------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    vim \
    udev \
    python3-pip \
    \
    ros-humble-desktop \
    ros-humble-cartographer-ros \
    ros-humble-slam-toolbox \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    \
    # -----------------------------------------------------
    # Vision / ArUco
    # -----------------------------------------------------
    libusb-1.0-0 \
    libusb-1.0-0-dev \
    libuvc-dev \
    libudev-dev \
    ros-humble-vision-msgs \
    ros-humble-image-transport \
    ros-humble-image-publisher \
    ros-humble-cv-bridge \
    ros-humble-camera-info-manager \
    ros-humble-aruco-ros \
    \
 && rm -rf /var/lib/apt/lists/*


# ---------------------------------------------------------
# YDLIDAR SDK
# ---------------------------------------------------------
WORKDIR /tmp
RUN git clone https://github.com/YDLIDAR/YDLidar-SDK.git && \
    mkdir -p YDLidar-SDK/build && \
    cd YDLidar-SDK/build && \
    cmake .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig && \
    rm -rf /tmp/YDLidar-SDK


# ---------------------------------------------------------
# YOLO (CPUベース推論のみ)
#
# ・ ultralytics は GPU 非依存のため Dockerfile に含める
#    (CPU でも動作可能, GPU があれば自動利用)
#
# ・ torch / torchvision は CUDA(JetPack) 依存のため
#    Dockerfileに含めない
#
# ・ YOLO用venv（ROSと分離：aptとpipの依存衝突を防ぐため） 
# ---------------------------------------------------------
RUN apt-get update && apt-get install -y python3-venv && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install ultralytics



# ---------------------------------------------------------
# 作業ディレクトリ戻す
# ---------------------------------------------------------
WORKDIR /root/ros2_ws
 
 
# ---------------------------------------------------------
# 自動 source 設定
#
# ・ ROS2 本体
# ・ colcon build 後の workspace(存在する場合のみ)
# ---------------------------------------------------------
RUN echo "source /opt/ros/humble/setup.bash" >> /etc/bash.bashrc
RUN echo "if [ -f /root/ros2_ws/install/setup.bash ]; then source /root/ros2_ws/install/setup.bash; fi" >> /etc/bash.bashrc
