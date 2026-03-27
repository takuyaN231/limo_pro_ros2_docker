# =========================================================
# TechShare LIMO Pro
# ROS 2 Humble Docker Image
# =========================================================
#
#   - Dockerは実行環境のみを構築する
#   - workspace（ros2_ws）はbindで外部管理
#
# =========================================================

FROM ros:humble

# ---------------------------------------------------------
# 作業ディレクトリ
# ---------------------------------------------------------
# メーカー想定と操作感を合わせる
WORKDIR /root/ros2_ws

ENV DEBIAN_FRONTEND=noninteractive

# ---------------------------------------------------------
# 基本ツール + ROS2フルセット
# ---------------------------------------------------------
# ros:humble は ros-core なので、
# desktop + slam + navigation を明示追加する
#
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
    # Vision / Camera / ArUco 系（教材対応）
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
 && rm -rf /var/lib/apt/lists/*


# ---------------------------------------------------------
# AI / YOLO (推論フレームワークのみ)
# ---------------------------------------------------------
#
# ultralytics は GPU 非依存のため Dockerfile に含める
#   - CPUでも動作可能
#   - GPUがあれば自動利用
#
# torch / torchvision は CUDA (JetPack) 依存のため
# Dockerfileには書かない
# Jetson Nano / Orin Nano で CUDAバージョンが異なるため
# ここで固定しない
#
RUN pip3 install --no-cache-dir ultralytics

# ---------------------------------------------------------
# 自動source（教育用）
# ---------------------------------------------------------
# 毎回 source 打たなくて済むようにする
#
RUN echo "source /opt/ros/humble/setup.bash" >> /etc/bash.bashrc

# ---------------------------------------------------------
# 注意：
# ---------------------------------------------------------
# ・limo_ros2 の clone はここに書かない
# ・colcon build もしない
# ・workspaceはbind前提
#
# ---------------------------------------------------------
