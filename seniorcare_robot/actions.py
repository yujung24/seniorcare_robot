import py_trees
from rclpy.node import Node

class TryTalk(py_trees.behaviour.Behaviour):
    def __init__(self, node: Node):
        super().__init__(name="TryTalk")
        self.node = node

    def initialise(self):
        self.node.get_logger().info("[BT] TryTalk initialise")

    def update(self):
        self.node.get_logger().info("[BT] TryTalk running")

        return py_trees.common.Status.RUNNING


class RunActionRecognition(py_trees.behaviour.Behaviour):
    def __init__(self, node: Node):
        super().__init__(name="RunActionRecognition")
        self.node = node

    def initialise(self):
        self.node.get_logger().info("[BT] RunActionRecognition initialise")

    def update(self):
        self.node.get_logger().info("[BT] RunActionRecognition running")
        pass
        return py_trees.common.Status.RUNNING
