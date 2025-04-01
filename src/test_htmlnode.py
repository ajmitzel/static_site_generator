import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("tag", "value", 3, {"href": "website", "a": "anchor"})
        node2 = HTMLNode("This is a text node", TextType.BOLD)

        print(node)
        print(node.props_to_html())

        #self.assertNotEqual(node2, node3)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
if __name__ == "__main__":
    unittest.main()