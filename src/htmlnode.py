class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        
        list_of_tuples = self.props.items()
        return " "+" ".join([n[0]+'="'+n[1]+'"' for n in list_of_tuples])
    
    def __repr__(self):
        return(f"HTML node:\n\t{self.tag}\n\t{self.value}\n\t{self.children}\n\t{self.props}\n")
    
class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):

        if self.value is None:
            raise ValueError("leaf nodes cannot have value=None")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    