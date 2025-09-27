import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print(f"------ TextNode tests x5: -------")
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a differet text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_noteq_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_noteq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url="testurl")
        node2 = TextNode("This is a text node", TextType.BOLD, url="also a url")
        self.assertNotEqual(node, node2)

    def test_noteq_missing_url(self):
        node = TextNode("This is a text node", TextType.BOLD, url="testurl")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

class TestHTMLNode(unittest.TestCase):


    plain_node= TextNode(text="plain text", text_type=TextType.TEXT)
    bold_node= TextNode(text="bold text", text_type=TextType.BOLD)
    italic_node= TextNode(text="italic text", text_type=TextType.ITALIC)
    code_node= TextNode(text="code text", text_type=TextType.CODE)
    link_node= TextNode(text="link text", text_type=TextType.LINK, url="alink.com")
    image_node= TextNode(text="alt text", text_type=TextType.IMAGE, url="image.jpg")
    
    cases = {"plain text": plain_node,
             "bold text": bold_node,
             "italic text": italic_node,
             "code text": code_node,
             "link text": link_node,
             "": image_node
    }
    
    def test_text(self):
        print(f"------ testing func: text_node_to_html_node -------")
        for c in self.cases:
            print(f"\tcase: {c}")
            node = self.cases[c]
            html_node = text_node_to_html_node(node)

            if "link" not in c and len(c)>0:
                self.assertEqual(html_node.props, None)
            else:
                self.assertIsNotNone(html_node.props)
            
            match node.text_type:
                case TextType.TEXT: t=None
                case TextType.BOLD: t="t"
                case TextType.ITALIC: t="i"
                case TextType.CODE: t="code"
                case TextType.LINK: t="a"
                case TextType.IMAGE: t="img"
                case _: raise ValueError("unrecognised text_type")

            self.assertEqual(html_node.tag, t)
            self.assertEqual(html_node.value, c)


if __name__ == "__main__":
    unittest.main()