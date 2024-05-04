import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode(value="test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode(value="test", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(len(node.props), 2)
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="a", props={"href", "https://example.com"})

    def test_to_html_no_tag(self):
        node = LeafNode(value="test")
        self.assertEqual(node.to_html(), "test")

    def test_to_html(self):
        node = LeafNode(tag="p", value="test")
        self.assertEqual(node.to_html(), "<p>test</p>")

    def test_to_html_with_props(self):
        node = LeafNode(tag="a", value="test", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://example.com" target="_blank">test</a>')

class TestParentNode(unittest.TestCase):
    def test_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(children=[LeafNode(value="test")])

    def test_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="p")

        with self.assertRaises(ValueError):
            ParentNode(tag="p", children=[])

    def test_to_html(self):
        node = ParentNode("p", [
            LeafNode("b", "Hello!"),
            LeafNode(None, " You should check out my "),
            LeafNode("i", "amazing"),
            LeafNode(None, " "),
            LeafNode("a", "website", {"href": "https://example.com"}),
            LeafNode(None, "!")
        ])

        self.assertEqual(node.to_html(), '<p><b>Hello!</b> You should check out my <i>amazing</i> <a href="https://example.com">website</a>!</p>')

    def test_to_html_nested(self):
        node = ParentNode("p", [
            LeafNode(None, "Hello! You should check out my "),
            ParentNode("b", [
                LeafNode("i", "amazing"),
                LeafNode(None, " new ")
            ]),
            LeafNode("a", "website", {"href": "https://example.com"}),
            LeafNode(None, "!")
        ])

        self.assertEqual(node.to_html(), '<p>Hello! You should check out my <b><i>amazing</i> new </b><a href="https://example.com">website</a>!</p>')

