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

import time

from demo_py.talker import Talker

def test_talker_rate():
    rclpy.init()
    node = Talker()

    stamps = []
    node.create_subscription(
        String, 'demo_chatter', lambda m: stamps.append(time.time()), 10)
    deadline = time.time() + 5.0
    while time.time() < deadline and len(stamps) < 4:
        rclpy.spin_once(node, timeout_sec=0.05)

    node.destroy_node()
    rclpy.try_shutdown()

    assert len(stamps) >= 4, f'只收到 {len(stamps)} 条，太少了'
    gaps = [b - a for a, b in zip(stamps, stamps[1:])]
    avg = sum(gaps) / len(gaps)
    assert 0.4 < avg < 0.6, f'期望间隔约 0.5 秒，实际 {avg:.2f} 秒'