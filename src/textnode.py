from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):

        if type(self) != type(other):
            raise TypeError("trying to compare objects of different classes")

        return (self.text == other.text
            and self.text_type == other.text_type 
            and self.url == other.url)
    
    def __repr__(self):
        return(f"TextNode({self.text}, {self.text_type.value}, {self.url})")


def text_node_to_html_node(text_node):

    match text_node.text_type:
        case TextType.TEXT: return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD: return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC: return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE: return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK: return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE: return LeafNode(tag="img", value="", props={"scr":text_node.url, "alt":text_node.text})  
        case _: raise ValueError("unrecognised text_type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    #tag_types = {"b": TextType.BOLD, "i": TextType.ITALIC, "code": TextType.CODE, "a": TextType.LINK, "img": TextType.IMAGE}
    
    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text_to_split = node.text
        if delimiter in text_to_split:
            split_text = text_to_split.split(delimiter)
        else:
            new_nodes.append(node)
            continue

        if len(split_text)%2 != 1:
            raise SyntaxError("invalid markdown syntax: missing closing delimiter")

        for i in range(len(split_text)):
            if i%2 == 0:
                new_nodes.append(TextNode(text=split_text[i], text_type=node.text_type))
            else:
                new_nodes.append(TextNode(text=split_text[i], text_type=text_type))

    return new_nodes


