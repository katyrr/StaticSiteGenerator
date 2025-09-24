import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    example_props = {
            "href": "alink.com",
            "target": "_blank",
        }

    node_all_none = HTMLNode()
    node_just_tag = HTMLNode(tag="a tag")
    node_just_value = HTMLNode(value="a value")
    node_just_children = HTMLNode(children=[node_all_none, node_just_tag])
    node_just_props = HTMLNode(props=example_props)
    node_no_none = HTMLNode(tag="another tag", value="another value", children=[node_just_value, node_just_props], props=example_props)

    cases = {
        "node_all_none":node_all_none, 
        "node_just_props":node_just_props, 
        "node_just_children":node_just_children, 
        "node_just_tag":node_just_tag, 
        "node_just_value":node_just_value, 
        "node_no_none":node_no_none
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
                expected = None
            self.assertEqual(joined, expected)

    def test_to_html(self):

        for case in self.cases:
            print(f"testing: {case}")
            c = self.cases[case]
        
            with self.assertRaises(NotImplementedError):
                c.to_html()


if __name__ == "__main__":
    unittest.main()