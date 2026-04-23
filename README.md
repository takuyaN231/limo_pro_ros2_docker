# LIMO ROS2 Humble Docker Environment
 
・DockerによるLIMO用ROS2環境
・再現性・共有性を目的とする
 
# 導入

・ROSの署名鍵をkeyring方式で登録（推奨）
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc -o ros.asc
gpg --dearmor ros.asc
sudo mv ros.asc.gpg /usr/share/keyrings/ros-archive-keyring.gpg
rm -f ros.asc
 
# ROS1リポジトリ（必要な場合のみ）
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://mirrors.tuna.tsinghua.edu.cn/ros/ubuntu focal main" > /etc/apt/sources.list.d/ros-latest.list'
 
# ROS2リポジトリ設定
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu focal main" > /etc/apt/sources.list.d/ros2-latest.list'
 
# Husarnet（不要なため削除）
sudo rm -f /etc/apt/sources.list.d/husarnet.list
 
# パッケージ更新
sudo apt update
 
# Dockerインストール
sudo apt install -y docker.io
 
# 動作確認
sudo docker run hello-world
 
# バージョン確認
docker --version
 
# sudo無しでdocker実行できるようにする
sudo usermod -aG docker $USER

# 再起動
sudo reboot
 
# docker-composeインストール
sudo apt install -y docker-compose
 
# バージョン確認
docker-compose --version
 
# ROS2 Humbleコンテナ起動テスト
docker run -it --rm ros:humble bash
 
# コンテナ内確認
echo $ROS_DISTRO
exit

