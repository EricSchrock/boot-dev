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
        self.assertEqual([node], node.split())

    def test_split_unmatched_delimiter(self):
        with self.assertRaises(ValueError):
            TextNode("Test **test test", "text").split()

        with self.assertRaises(ValueError):
            TextNode("Test **test* test", "text").split()

    def test_split_nothing_to_split(self):
        node = TextNode("Test", "text")
        self.assertEqual([node], node.split())

    def test_split_bold_in_middle(self):
        self.assertEqual(TextNode("Test **test** test", "text").split(), [
            TextNode("Test ", "text"),
            TextNode("test", "bold"),
            TextNode(" test", "text"),
        ])

    def test_split_italic_at_start(self):
        self.assertEqual(TextNode("*Test* test", "text").split(), [
            TextNode("Test", "italic"),
            TextNode(" test", "text"),
        ])

    def test_split_all_code(self):
        self.assertEqual(TextNode("`Test test`", "text").split(), [
            TextNode("Test test", "code"),
        ])

    def test_split_code_at_end(self):
        self.assertEqual(TextNode("Test `test`", "text").split(), [
            TextNode("Test ", "text"),
            TextNode("test", "code"),
        ])

    def test_split_mulitple_code_blocks(self):
        self.assertEqual(TextNode("Test `test``test`", "text").split(), [
            TextNode("Test ", "text"),
            TextNode("test", "code"),
            TextNode("test", "code"),
        ])

    def test_split_image_in_middle(self):
        self.assertEqual(TextNode("Text with an ![image](https://example.com) and such", "text").split(), [
            TextNode("Text with an ", "text"),
            TextNode("image", "image", "https://example.com"),
            TextNode(" and such", "text"),
        ])

    def test_split_image_at_start(self):
        self.assertEqual(TextNode("![image](https://example.com) and such", "text").split(), [
            TextNode("image", "image", "https://example.com"),
            TextNode(" and such", "text"),
        ])

    def test_split_image_at_end(self):
        self.assertEqual(TextNode("Text with an ![image](https://example.com)", "text").split(), [
            TextNode("Text with an ", "text"),
            TextNode("image", "image", "https://example.com"),
        ])

    def test_split_just_image(self):
        self.assertEqual(TextNode("![image](https://example.com)", "text").split(), [
            TextNode("image", "image", "https://example.com"),
        ])

    def test_split_mulitple_images(self):
        self.assertEqual(TextNode("Hi there ![hello](https://hello.com) and ![example](https://example.com)", "text").split(), [
            TextNode("Hi there ", "text"),
            TextNode("hello", "image", "https://hello.com"),
            TextNode(" and ", "text"),
            TextNode("example", "image", "https://example.com"),
        ])

    def test_split_multiple_types(self):
        self.assertEqual(TextNode("Test **bold** advances in `code` and such", "text").split(), [
            TextNode("Test ", "text"),
            TextNode("bold", "bold"),
            TextNode(" advances in ", "text"),
            TextNode("code", "code"),
            TextNode(" and such", "text"),
        ])

    def test_extract_images(self):
        node = TextNode("Text with ![two](https://example.com) ![images](https://example.com) and also a [couple](https://example.com) [links](https://example.com)", "text")
        self.assertEqual(node.extract_images(), [("two", "https://example.com"), ("images", "https://example.com")])

    def test_extract_links(self):
        node = TextNode("Text with ![two](https://example.com) ![images](https://example.com) and also a [couple](https://example.com) [links](https://example.com)", "text")
        self.assertEqual(node.extract_links(), [("couple", "https://example.com"), ("links", "https://example.com")])

if __name__ == "__main__":
    unittest.main()
