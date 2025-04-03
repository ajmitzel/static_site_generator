from enum import Enum
from htmlnode import HTMLNode
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "normal text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code"
    LINK = "links"
    IMAGE = "images"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, text_node):
        if self.text == text_node.text and self.text_type.value == text_node.text_type.value and self.url == text_node.url:
            return True
        return False

    def __repr__(self):
        return "TextNode({}, {}, {})".format(self.text, self.text_type.value, self.url)

def text_node_to_html_node(node):
    if node.text_type.value not in [e.value for e in TextType]:
        raise Exception("text type not recognized")

    if node.text_type == TextType.TEXT:
        return LeafNode(None, node.text)
    elif node.text_type == TextType.BOLD:
        return LeafNode("b", node.text)
    elif node.text_type == TextType.ITALIC:
        return LeafNode("i", node.text)
    elif node.text_type == TextType.CODE:
        return LeafNode("code", node.text)
    elif node.text_type == TextType.LINK:
        return LeafNode("a", node.text, {"href": node.url})
    else:
        return LeafNode("img", "", {"src": node.url, "alt": node.text})