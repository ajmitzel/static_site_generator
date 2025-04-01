from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return self.value
        else:
            front_tag = "<{}".format(self.tag)
            if self.props == None:
                front_tag += ">"
            else:
                for prop in self.props.keys():
                    front_tag += " {}=\"{}\"".format(prop, self.props[prop])
                front_tag += ">"
            return "{}{}</{}>".format(front_tag, self.value, self.tag)

            