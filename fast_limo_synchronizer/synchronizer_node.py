import rclpy
from rclpy.node import Node, QoSProfile, TimeSource
from rclpy.time import Time, Duration
from sensor_msgs.msg import Imu, PointCloud2
from std_msgs.msg import Int32,UInt32

class Synchronizer(Node):

    def __init__(self):
        super().__init__('synchronizer')
        self.start_time = self.get_clock().now()
        self.zero_time = Time(seconds=0,nanoseconds=0)

        self.imu_msg_sub = self.create_subscription(
            msg_type=Imu,
            topic="/imu/data",
            callback=self.imu_msg_callback,
            qos_profile=10
        )
        self.lidar_msg_sub = self.create_subscription(
            msg_type=PointCloud2,
            topic="/lidar_points",
            callback=self.lidar_msg_callback,
            qos_profile=10
        )

        self.imu_pub = self.create_publisher(
            msg_type=Imu,
            topic="/imu/sync_data",
            qos_profile=10
        )
        self.lidar_pub = self.create_publisher(
            msg_type=PointCloud2,
            topic="/lidar_sync_points",
            qos_profile=10
        )

    def imu_msg_callback(self, msg):
        elapsed_time = self.zero_time + (self.get_clock().now() - self.start_time)
        actual_elapsed_time = Time(seconds=elapsed_time.seconds_nanoseconds()[0], nanoseconds=elapsed_time.seconds_nanoseconds()[1])
        msg.header.stamp = actual_elapsed_time.to_msg()
        self.get_logger().info(f"IMU msg timestamp:\n{msg.header.stamp}")
        self.imu_pub.publish(msg)


    def lidar_msg_callback(self, msg):
        elapsed_time = self.zero_time + (self.get_clock().now() - self.start_time)
        actual_elapsed_time = Time(seconds=elapsed_time.seconds_nanoseconds()[0], nanoseconds=elapsed_time.seconds_nanoseconds()[1])
        msg.header.stamp = actual_elapsed_time.to_msg()
        self.get_logger().info(f"LIDAR msg timestamp:\n{msg.header.stamp}")
        self.lidar_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    synchronizer_subscriber = Synchronizer()

    rclpy.spin(synchronizer_subscriber)

    synchronizer_subscriber.destroy_node()
    rclpy.shutdown()