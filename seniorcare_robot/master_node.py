import rclpy
from rclpy.node import Node
from rclpy.qos import (
    QoSProfile,
    QoSReliabilityPolicy,
    QoSHistoryPolicy,
    QoSDurabilityPolicy,
)
from std_msgs.msg import Float64MultiArray
from math import pi

import py_trees

import argparse
import sys


from seniorcare_robot.conditions import (
    IsTalkRequested,
    IsPoseRecogRequested,
    IsMode1Selected,
)

from seniorcare_robot.actions import (
    TryTalk,
    RunActionRecognition,
)

class StatePublisher(Node):
    def __init__(self):
        super().__init__('state_publisher')

        qos_profile = QoSProfile(depth=10)
        qos_realiable = QoSProfile(history=QoSHistoryPolicy.KEEP_LAST,
                                   depth=10,
                                   reliability=QoSReliabilityPolicy.BEST_EFFORT,
                                   durability=QoSDurabilityPolicy.VOLATILE)

        self.state_publisher_ = self.create_publisher(Float64MultiArray, "state", qos_profile)

        self.tracking_mode = 1
        self.pose_recog_requested = False
        self.talk_requested = False

        self.tree = self.create_behavior_tree()

        # def LiDAR_callback():

    def create_behavior_tree(self):
        # Event 2: Talk
        talk_branch = py_trees.composites.Sequence(name="TALK_BRANCH", memory=False)
        talk_branch.add_children(
            [
                IsTalkRequested(self),
                TryTalk(self),
            ]
        )
        # Event 1: Action Recognition
        action_recog_branch = py_trees.composites.Sequence(
            name="ACTION_RECOG_BRANCH", memory=False
        )
        action_recog_branch.add_children(
            [
                IsPoseRecogRequested(self),
                RunActionRecognition(self),
            ]
        )
        # Mode 1: User Tracking
        mode1_branch = py_trees.composites.Sequence(
            name="MODE1_TRACKING_BRANCH", memory=False
        )
        mode1_branch.add_children(
            [
                IsMode1Selected(self),

            ]
        )

        root = py_trees.composites.Selector(name="ROOT", memory=False)
        root.add_children(
            [
                talk_branch,
                action_recog_branch,
            ]
        )

        tree = py_trees.trees.BehaviourTree(root=root)
        tree.setup(timeout=15)
        return tree

    def tick_tree(self):
        self.tree.tick()

        self.get_logger().info(
            f"[STATE] mode={self.tracking_mode}, "
            f"talk={self.talk_requested}, "
            f"action={self.pose_recog_requested}, "
        )


def main(args=None):
    rclpy.init(args=args)
    node = StatePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\n killed with ctrl-c ")
    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    if not main():
        sys.exit(1)
