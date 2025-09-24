import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):

    example_props = {
            "href": "alink.com",
            "target": "_blank",
        }

    node_all_none = HTMLNode()
    node_just_tag = HTMLNode(tag="a")
    node_just_value = HTMLNode(value="a value")
    node_just_children = HTMLNode(children=[node_all_none, node_just_tag])
    node_just_props = HTMLNode(props=example_props)
    node_no_none = HTMLNode(tag="t", value="another value", children=[node_just_value, node_just_props], props=example_props)
    leaf_node_plain = LeafNode(tag="p", value="some text")
    leaf_node_attributed = LeafNode(tag="a", value="click here", props=example_props)
    leaf_node_no_tag = LeafNode(tag=None, value="val")

    cases = {
        "node_all_none":node_all_none, 
        "node_just_props":node_just_props, 
        "node_just_children":node_just_children, 
        "node_just_tag":node_just_tag, 
        "node_just_value":node_just_value, 
        "node_no_none":node_no_none,
        "leaf_node_plain":leaf_node_plain,
        "leaf_node_attributed":leaf_node_attributed,
        "leaf_node_no_tag":leaf_node_no_tag
    }

    def test_props_to_html(self):
        
        for case in self.cases:
            print(f"-------------------- testing: {case}--------------------")
            c = self.cases[case]
            print(c)
            joined = c.props_to_html()
            if c.props is not None:
                expected =  ' href="alink.com" target="_blank"'
            else:
                expected = ""
            self.assertEqual(joined, expected)

    def test_to_html(self):

        for case in self.cases:
            print(f"testing: {case}")
            c = self.cases[case]

            if type(c)==LeafNode:

                match case:
                    case "leaf_node_plain": expected = "<p>some text</p>"
                    case "leaf_node_attributed": expected = '<a href="alink.com" target="_blank">click here</a>'
                    case "leaf_node_no_tag": expected = "val"
                    case _: raise RuntimeError("haven't provided expected value")

                self.assertEqual(c.to_html(), expected)
            
            else:
                with self.assertRaises(NotImplementedError):
                    c.to_html()


if __name__ == "__main__":
    unittest.main()