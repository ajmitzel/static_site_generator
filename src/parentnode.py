from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError
        elif self.children == None:
            raise ValueError("Parent Node Missing Leaf Nodes")
        else:
            content = ""
            front_tag = "<{}".format(self.tag)
            if self.props == None:
                front_tag += ">"
            else:
                for prop in self.props.keys():
                    front_tag += " {}=\"{}\"".format(prop, self.props[prop])
                front_tag += ">"

            content = front_tag

            for node in self.children:
                content += node.to_html()
            return content + "</{}>".format(self.tag)

