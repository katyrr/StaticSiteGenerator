import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_link, split_nodes_image


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        print(f"\n------ TextNode tests x5: -------")
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
        print(f"\n------ testing func: text_node_to_html_node -------")
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
                case TextType.BOLD: t="b"
                case TextType.ITALIC: t="i"
                case TextType.CODE: t="code"
                case TextType.LINK: t="a"
                case TextType.IMAGE: t="img"
                case _: raise ValueError("unrecognised text_type")

            self.assertEqual(html_node.tag, t)
            self.assertEqual(html_node.value, c)


class Test_split_nodes(unittest.TestCase):

    bold_cases = {
        "This **text is** bold": [
            TextNode("This ", TextType.TEXT),
            TextNode("text is", TextType.BOLD),
            TextNode(" bold", TextType.TEXT),
        ],
        "This is plain text": [
            TextNode("This is plain text", TextType.TEXT),
        ],
        "This **has** multiple **bold** sections": [
            TextNode("This ", TextType.TEXT),
            TextNode("has", TextType.BOLD),
            TextNode(" multiple ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" sections", TextType.TEXT),
        ]
    }

    def test_bold_individuals(self):
        print(f"\n------ testing func: split_node_delimiter, for individual bold cases -------")
        for c in self.bold_cases:
            print(f"\tcase: {c}")
            old_node = TextNode(c, TextType.TEXT)
            result = split_nodes_delimiter([old_node], "**", TextType.BOLD)
            self.assertEqual(result, self.bold_cases[c])

    def test_missing_delimiter_error(self):
        print(f"\n------ testing func: split_node_delimiter, for expected errors ------")

        print(f"\tcase: missing closing delimiter")
        missing_delimiter_node = TextNode("This is **missing a closing delimiter", TextType.TEXT)

        with self.assertRaises(SyntaxError):
            split_nodes_delimiter([missing_delimiter_node], "**", TextType.BOLD)

    def test_other_delimiters(self):
        print(f"\n------ testing func: split_node_delimiter, for italic and code blocks ------")

        print(f"\tcase: italic node")
        italic_node = TextNode("This _is some_ italic text", TextType.TEXT)
        new_italic_node = split_nodes_delimiter([italic_node], "_", TextType.ITALIC)
        self.assertEqual(new_italic_node, [
            TextNode("This ", TextType.TEXT),
            TextNode("is some", TextType.ITALIC),
            TextNode(" italic text", TextType.TEXT),
        ])

        print(f"\tcase: code node")
        code_node = TextNode("`This is` some code text", TextType.TEXT)
        new_code_node = split_nodes_delimiter([code_node], "`", TextType.CODE)
        self.assertEqual(new_code_node, [
            TextNode("", TextType.TEXT),
            TextNode("This is", TextType.CODE),
            TextNode(" some code text", TextType.TEXT),
        ])

        print(f"\tcase: node already attributed")
        attributed_node = TextNode("This _node_ is already bold", TextType.BOLD)
        new_attributed_node = split_nodes_delimiter([attributed_node], "_", TextType.ITALIC)
        self.assertEqual(new_attributed_node, [attributed_node])

    def test_link_delimiters(self):

        print(f"\n------ testing func: split_nodes_link ------")
        
        print(f"\tcase: two links one at end")
        node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]

        self.assertEqual(new_nodes, expected)

        print(f"\tcase: two links one at start")
        node = TextNode(
        "[link to boot dev](https://www.boot.dev) and [link to youtube](https://www.youtube.com/@bootdotdev) both embedded",
        TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(" both embedded", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)

        print(f"\tcase: two links no text")
        node = TextNode(
        "[link to boot dev](https://www.boot.dev)[link to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("link to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode("link to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]

        self.assertEqual(new_nodes, expected)

        print(f"\tcase: no links")
        node = TextNode("just some plain text", TextType.TEXT)

        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("just some plain text", TextType.TEXT)
        ]

        self.assertListEqual(new_nodes, expected)

    def test_split_images(self):
        print(f"\n------ testing func: split_nodes_image ------")
        
        print(f"\tcase: two images one at end")
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
        self.assertListEqual(expected, new_nodes)
        

        
class test_extract_images_and_links(unittest.TestCase):

    def test_extract_images(self):
        print(f"\n------ testing func: image extraction ------")

        print(f"\tcase: simple two images")
        test_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(test_text)

        expected_result = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        
        self.assertListEqual(result, expected_result)

        print(f"\tcase: missing syntax - alt text")
        missing_text = "This image is missing ](image.jpg) alt text"
        with self.assertRaises(SyntaxError):
            result = extract_markdown_images(missing_text)


        print(f"\tcase: missing syntax - image url")
        missing_url = "This ![image]( is missing a url"
        with self.assertRaises(SyntaxError):
            result = extract_markdown_images(missing_url)

        print(f"\tcase: no image found")
        plain_text = "some text with no image"
        result = extract_markdown_images(plain_text)
        self.assertEqual(len(result), 0)


    def test_extract_links(self):
        print(f"\n------ testing func: link extraction ------")

        print(f"\tcase: simple two links")
        test_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        result = extract_markdown_links(test_text)

        expected_result = [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        
        self.assertListEqual(result, expected_result)

        print(f"\tcase: missing syntax - link text")
        missing_text = "This link is missing ](image.jpg) text"
        with self.assertRaises(SyntaxError):
            result = extract_markdown_images(missing_text)


        print(f"\tcase: missing syntax - url")
        missing_url = "This ![link]( is missing a url"
        with self.assertRaises(SyntaxError):
            result = extract_markdown_images(missing_url)

        print(f"\tcase: no link found")
        plain_text = "some text with no link"
        result = extract_markdown_images(plain_text)
        self.assertEqual(len(result), 0)
        






if __name__ == "__main__":
    unittest.main()