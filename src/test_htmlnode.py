import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
    parent_node_only_leaves = ParentNode(tag="t", children=[leaf_node_attributed, leaf_node_no_tag, leaf_node_plain])
    parent_node_with_subparents = ParentNode(tag="a", children=[leaf_node_no_tag, parent_node_only_leaves, leaf_node_plain])

    cases = {
        "node_all_none":node_all_none, 
        "node_just_props":node_just_props, 
        "node_just_children":node_just_children, 
        "node_just_tag":node_just_tag, 
        "node_just_value":node_just_value, 
        "node_no_none":node_no_none,
        "leaf_node_plain":leaf_node_plain,
        "leaf_node_attributed":leaf_node_attributed,
        "leaf_node_no_tag":leaf_node_no_tag,
        "parent_node_only_leaves":parent_node_only_leaves,
        "parent_node_with_subparents":parent_node_with_subparents
    }

    def test_props_to_html(self):
        print(f"------ testing method: props_to_html -------")
        for case in self.cases:
            print(f"\tcase: {case}")
            c = self.cases[case]
            #print(c)
            joined = c.props_to_html()
            if c.props is not None:
                expected =  ' href="alink.com" target="_blank"'
            else:
                expected = ""
            self.assertEqual(joined, expected)

    def test_to_html(self):
        print(f"------ testing method: to_html -------")

        for case in self.cases:
            print(f"\tcase: {case}")
            c = self.cases[case]

            if type(c)==LeafNode:

                match case:
                    case "leaf_node_plain": expected = "<p>some text</p>"
                    case "leaf_node_attributed": expected = '<a href="alink.com" target="_blank">click here</a>'
                    case "leaf_node_no_tag": expected = "val"
                    case _: raise RuntimeError("haven't provided expected value")

                self.assertEqual(c.to_html(), expected)
            
            elif type(c)==ParentNode:

                match case:
                    case "parent_node_only_leaves": expected = '<t><a href="alink.com" target="_blank">click here</a>val<p>some text</p></t>'
                    case "parent_node_with_subparents": expected = '<a>val<t><a href="alink.com" target="_blank">click here</a>val<p>some text</p></t><p>some text</p></a>'
            
                self.assertEqual(c.to_html(), expected)


            else:
                with self.assertRaises(NotImplementedError):
                    c.to_html()

    
        


if __name__ == "__main__":
    unittest.main()