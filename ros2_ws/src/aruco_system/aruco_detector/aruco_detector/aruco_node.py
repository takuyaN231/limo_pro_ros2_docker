import rclpy
from rclpy.node import Node
 
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseStamped
 
from cv_bridge import CvBridge
 
import cv2
import cv2.aruco as aruco
import numpy as np
 
# 姿勢変換用
from scipy.spatial.transform import Rotation as R
 
 
class ArucoNode(Node):
    def __init__(self):
        super().__init__('aruco_node')
 
        # ===== parameters =====
        self.declare_parameter('dictionary', 'DICT_6X6_1000')
        self.declare_parameter('marker_size', 0.10)
        self.declare_parameter('target_id', 300)
 
        self.dictionary_name = self.get_parameter('dictionary').value
        self.marker_size = self.get_parameter('marker_size').value
        self.target_id = self.get_parameter('target_id').value
 
        # ===== aruco =====
        self.aruco_dict = getattr(aruco, self.dictionary_name)
        self.dictionary = aruco.getPredefinedDictionary(self.aruco_dict)
        self.parameters = aruco.DetectorParameters_create()
 
        # ===== ROS =====
        self.bridge = CvBridge()
 
        self.create_subscription(
            Image,
            '/camera/color/image_raw',
            self.image_callback,
            10
        )
 
        self.create_subscription(
            CameraInfo,
            '/camera/color/camera_info',
            self.camera_info_callback,
            10
        )
 
        # publishers
        self.pub_found = self.create_publisher(Bool, '/aruco/target_found', 10)
        self.pub_pose = self.create_publisher(PoseStamped, '/aruco/target_pose', 10)
        self.pub_debug = self.create_publisher(Image, '/aruco/debug_image', 10)
 
        # camera params
        self.camera_matrix = None
        self.dist_coeffs = None
 
        # state
        self.last_found = False
 
        self.get_logger().info('Aruco detector started')
        self.get_logger().info(f'dictionary: {self.dictionary_name}')
        self.get_logger().info(f'target_id: {self.target_id}')
 
    def camera_info_callback(self, msg):
        if self.camera_matrix is None:
            self.camera_matrix = np.array(msg.k).reshape(3, 3)
            self.dist_coeffs = np.array(msg.d)
            self.get_logger().info('Camera info received')
 
    def image_callback(self, msg):
        if self.camera_matrix is None:
            return
 
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
 
        corners, ids, _ = aruco.detectMarkers(
            frame,
            self.dictionary,
            parameters=self.parameters
        )
 
        found = False
 
        if ids is not None:
            ids_list = ids.flatten().tolist()
 
            # debug描画
            aruco.drawDetectedMarkers(frame, corners, ids)
 
            if self.target_id in ids_list:
                found = True
 
                index = ids_list.index(self.target_id)
 
                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
                    [corners[index]],
                    self.marker_size,
                    self.camera_matrix,
                    self.dist_coeffs
                )
 
                # ===== Pose作成 =====
                pose_msg = PoseStamped()
                pose_msg.header = msg.header
 
                # 位置
                pose_msg.pose.position.x = float(tvec[0][0][0])
                pose_msg.pose.position.y = float(tvec[0][0][1])
                pose_msg.pose.position.z = float(tvec[0][0][2])
 
                # ===== rvec → quaternion =====
                rmat, _ = cv2.Rodrigues(rvec[0])
                quat = R.from_matrix(rmat).as_quat()  # [x, y, z, w]
 
                pose_msg.pose.orientation.x = float(quat[0])
                pose_msg.pose.orientation.y = float(quat[1])
                pose_msg.pose.orientation.z = float(quat[2])
                pose_msg.pose.orientation.w = float(quat[3])
 
                self.pub_pose.publish(pose_msg)
 
        # ===== found topic =====
        found_msg = Bool()
        found_msg.data = found
        self.pub_found.publish(found_msg)
 
        # ===== 状態変化ログ =====
        if found and not self.last_found:
            self.get_logger().info('Target acquired')
 
        if not found and self.last_found:
            self.get_logger().info('Target lost')
 
        self.last_found = found
 
        # ===== debug image =====
        debug_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        debug_msg.header = msg.header
        self.pub_debug.publish(debug_msg)
 
 
def main(args=None):
    rclpy.init(args=args)
    node = ArucoNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
 
 
if __name__ == '__main__':
    main()
 
