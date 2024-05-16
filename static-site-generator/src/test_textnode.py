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

    def test_split_non_text(self):
        node = TextNode("Test", "code")
        self.assertEqual([node], node.split('*'))

    def test_split_invalid_delimiter(self):
        with self.assertRaises(ValueError):
            TextNode("Test", "text").split('_')

    def test_split_unmatched_delimiter(self):
        with self.assertRaises(ValueError):
            TextNode("Test **test test", "text").split('**')

        with self.assertRaises(ValueError):
            TextNode("Test **test* test", "text").split('**')

    def test_split_nothing_to_split(self):
        node = TextNode("Test", "text")
        self.assertEqual([node], node.split('*'))

    def test_split(self):
        self.assertEqual(TextNode("Test **test**", "text").split('**'), [TextNode("Test ", "text"), TextNode("test", "bold")])
        self.assertEqual(TextNode("*Test* test", "text").split('*'), [TextNode("Test", "italic"), TextNode(" test", "text")])
        self.assertEqual(TextNode("`Test test`", "text").split('`'), [TextNode("Test test", "code")])

    def test_split_order(self):
        node = TextNode("Test **bold** advances in `code` and such", "text")
        bold_first = node.split('**')
        code_first = node.split('`')
        self.assertNotEqual(bold_first, code_first)

        code_second = []
        for node in bold_first:
            code_second.extend(node.split('`'))

        bold_second = []
        for node in code_first:
            bold_second.extend(node.split('**'))

        self.assertEqual(code_second, bold_second)

    def test_extract_images(self):
        node = TextNode("Text with ![two](https://example.com) ![images](https://example.com) and also a [couple](https://example.com) [links](https://example.com)", "text")
        self.assertEqual(node.extract_images(), [("two", "https://example.com"), ("images", "https://example.com")])

    def test_extract_links(self):
        node = TextNode("Text with ![two](https://example.com) ![images](https://example.com) and also a [couple](https://example.com) [links](https://example.com)", "text")
        self.assertEqual(node.extract_links(), [("couple", "https://example.com"), ("links", "https://example.com")])

if __name__ == "__main__":
    unittest.main()
