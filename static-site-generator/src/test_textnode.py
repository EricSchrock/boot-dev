import unittest

from htmlnode import LeafNode
from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_invalid_text_type(self):
        with self.assertRaises(ValueError):
            TextNode("Text", "test")

    def test_missing_url(self):
        with self.assertRaises(ValueError):
            TextNode("Test", "link")

        with self.assertRaises(ValueError):
            TextNode("Test", "image")

    def test_unnecessary_url(self):
        with self.assertRaises(ValueError):
            TextNode("Test", "text", "https://example.com")

        with self.assertRaises(ValueError):
            TextNode("Test", "bold", "https://example.com")

        with self.assertRaises(ValueError):
            TextNode("Test", "italic", "https://example.com")

        with self.assertRaises(ValueError):
            TextNode("Test", "code", "https://example.com")

    def test_eq(self):
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_text_neq(self):
        node1 = TextNode("Hello", "bold")
        node2 = TextNode("Hi Hi", "bold")
        self.assertNotEqual(node1, node2)

    def test_text_type_neq(self):
        node1 = TextNode("Hello", "bold")
        node2 = TextNode("Hello", "italic")
        self.assertNotEqual(node1, node2)

    def test_url_neq(self):
        node1 = TextNode("Hello", "link", "https://example.com")
        node2 = TextNode("Hello", "link", "example.com")
        self.assertNotEqual(node1, node2)

    def test_to_html_node(self):
        text = TextNode("Hello", "text")
        html = LeafNode(value="Hello")
        self.assertEqual(text.to_html_node(), html)


if __name__ == "__main__":
    unittest.main()
