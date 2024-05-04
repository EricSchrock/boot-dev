import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_no_value_or_chilren(self):
        with self.assertRaises(RuntimeError):
            HTMLNode(tag="a", props={"href", "https://example.com"})

    def test_to_html(self):
        node = HTMLNode(value="test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(value="test", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(len(node.props), 2)
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = LeafNode(value="test")
        self.assertEqual(node.to_html(), "test")

    def test_to_html_no_props(self):
        node = LeafNode(tag="p", value="test")
        self.assertEqual(node.to_html(), "<p>test</p>")

    def test_to_html_props(self):
        node = LeafNode(tag="a", value="test", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">test</a>')
