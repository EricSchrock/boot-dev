import unittest

from htmlnode import HTMLNode

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
