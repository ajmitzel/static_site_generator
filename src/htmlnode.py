class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        total_attr = ""
        for attr in self.props:
            total_attr += " " + attr + "=\"" + self.props[attr] + "\""
        print(total_attr)
        return total_attr

    def __repr__(self):
        return "HTMLNode({}, {}, {}, {})".format(self.tag, self.value, self.children, self.props)
    