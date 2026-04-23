import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, PoseStamped
import math
 
 
class ArucoFollower(Node):
 
    def __init__(self):
        super().__init__('aruco_follower')
 
        # ===== 目標 =====
        self.goal_z = 0.40          # 安全側。まずは40cmで止める
        self.final_start = 0.55     # ここから最終進入モード
 
        # ===== 完了条件 =====
        self.x_done = 0.02
        self.yaw_done = 0.06        # 約3.4度
        self.z_done_tol = 0.03
 
        # ===== 安全条件 =====
        self.z_hard_stop = 0.32     # これより近ければ無条件停止
        self.yaw_no_forward = 0.12  # 約7度超なら前進禁止
        self.x_no_forward = 0.05    # 5cm超なら前進禁止
 
        # ===== ロスト対策 =====
        self.hold_time = 0.4
        self.lost_timeout = 1.0
        self.search_angular = 0.10
 
        # ===== 遠距離制御 =====
        self.k_x_far = 0.8
        self.k_yaw_far = 1.0
        self.linear_far = 0.08
        self.max_ang_far = 0.12
 
        # ===== 近距離制御 =====
        self.k_x_near = 1.2
        self.k_yaw_near = 1.6
        self.k_z_near = 0.5
        self.max_ang_near = 0.10
        self.linear_near_max = 0.03
        self.linear_near_min = -0.02
 
        # ===== 状態 =====
        self.done = False
 
        self.x = 0.0
        self.z = 1.0
        self.yaw = 0.0
 
        self.last_x = 0.0
        self.last_z = 1.0
        self.last_yaw = 0.0
 
        self.last_seen = self.get_clock().now()
 
        # ===== ROS =====
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.sub = self.create_subscription(
            PoseStamped,
            '/aruco/target_pose',
            self.cb,
            10
        )
 
        self.timer = self.create_timer(0.05, self.loop)
 
        self.get_logger().info("Aruco follower safe mode")
 
    def get_yaw(self, q):
        return math.atan2(
            2.0 * (q.w * q.y + q.x * q.z),
            1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        )
 
    def clamp(self, v, mn, mx):
        return max(mn, min(v, mx))
 
    def cb(self, msg):
        self.x = msg.pose.position.x
        self.z = msg.pose.position.z
        self.yaw = self.get_yaw(msg.pose.orientation)
 
        self.last_x = self.x
        self.last_z = self.z
        self.last_yaw = self.yaw
        self.last_seen = self.get_clock().now()
 
    def loop(self):
        msg = Twist()
 
        if self.done:
            self.pub.publish(msg)
            return
 
        now = self.get_clock().now()
        dt = (now - self.last_seen).nanoseconds / 1e9
 
        # ===== ロスト時 =====
        if dt > self.lost_timeout:
            msg.linear.x = 0.0
            msg.angular.z = self.search_angular
            self.pub.publish(msg)
            return
 
        # ===== 一時ロストはホールド =====
        if dt > self.hold_time:
            x = self.last_x
            z = self.last_z
            yaw = self.last_yaw
        else:
            x = self.x
            z = self.z
            yaw = self.yaw
 
        # ===== 絶対安全停止 =====
        if z <= self.z_hard_stop:
            self.get_logger().warn("HARD STOP")
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.done = True
            self.pub.publish(msg)
            return
 
        # ===== 完了判定 =====
        if abs(x) < self.x_done and abs(yaw) < self.yaw_done and abs(z - self.goal_z) < self.z_done_tol:
            self.get_logger().info("DONE")
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.done = True
            self.pub.publish(msg)
            return
 
        # ===== 遠距離：進みながら寄せる =====
        if z > self.final_start:
            angular = -(self.k_x_far * x + self.k_yaw_far * yaw)
            angular = self.clamp(angular, -self.max_ang_far, self.max_ang_far)
 
            msg.angular.z = angular
            msg.linear.x = self.linear_far
 
        # ===== 近距離：角度優先だが微修正しながら入る =====
        else:
            angular = -(self.k_x_near * x + self.k_yaw_near * yaw)
            angular = self.clamp(angular, -self.max_ang_near, self.max_ang_near)
 
            # 角度や横ズレが大きい時は前進禁止
            if abs(yaw) > self.yaw_no_forward or abs(x) > self.x_no_forward:
                linear = 0.0
            else:
                linear = -self.k_z_near * (z - self.goal_z)
                linear = self.clamp(linear, self.linear_near_min, self.linear_near_max)
 
            msg.angular.z = angular
            msg.linear.x = linear
 
        self.pub.publish(msg)
 
 
def main(args=None):
    rclpy.init(args=args)
    node = ArucoFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
 
 
if __name__ == '__main__':
    main()
