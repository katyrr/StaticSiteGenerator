import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
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


if __name__ == "__main__":
    unittest.main()