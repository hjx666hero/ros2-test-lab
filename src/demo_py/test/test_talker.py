"""End-to-end test: a publisher and a subscriber in one process must exchange a message.

This is the smallest useful "integration test" in ROS 2 and the template for the
robot-scenario tests you will write later.
"""
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


def test_publish_and_receive():
    rclpy.init()
    node = Node('demo_test_node')
    received = []
    node.create_subscription(
        String, 'demo_test_topic', lambda msg: received.append(msg.data), 10)
    pub = node.create_publisher(String, 'demo_test_topic', 10)

    deadline = time.time() + 5.0
    try:
        while time.time() < deadline and not received:
            msg = String()
            msg.data = 'ping'
            pub.publish(msg)
            rclpy.spin_once(node, timeout_sec=0.1)
    finally:
        node.destroy_node()
        rclpy.try_shutdown()

    assert received, 'no message received within 5s'
    assert received[0] == 'ping'
