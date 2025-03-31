from enum import Enum

class TextType(Enum):
    NORMAL = "normal text"
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