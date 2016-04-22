import unittest
import node


class TestNode(unittest.TestCase):

    def test_default_peers(self):
        self.assertEqual(len(node.Node()), 8)