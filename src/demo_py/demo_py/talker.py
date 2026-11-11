import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Talker(Node):

    def __init__(self):
        super().__init__('demo_talker')
        self.publisher_ = self.create_publisher(String, 'demo_chatter', 10)
        self.count = 0
        self.timer = self.create_timer(0.2, self.tick)

    def tick(self):
        msg = String()
        msg.data = f'hello from 黄嘉翔 #{self.count}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'publishing: "{msg.data}"')
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = Talker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
