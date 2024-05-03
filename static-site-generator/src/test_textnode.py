import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
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
        node1 = TextNode("Hello", "bold", "https://example.com")
        node2 = TextNode("Hello", "bold", "example.com")
        self.assertNotEqual(node1, node2)

    def test_one_missing_url(self):
        node1 = TextNode("Hello", "bold", "https://example.com")
        node2 = TextNode("Hello", "bold")
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()
