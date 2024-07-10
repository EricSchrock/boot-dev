import unittest

from htmlnode import LeafNode, ParentNode
from markdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title

three_blocks_with_heading = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""

three_blocks_with_multiline_paragraph = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""

class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks_example1(self):
        self.assertEqual(markdown_to_blocks(three_blocks_with_heading), [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item",
        ])

    def test_markdown_to_blocks_example2(self):
        self.assertEqual(markdown_to_blocks(three_blocks_with_multiline_paragraph), [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ])

    def test_markdown_to_blocks_leading_whitespace(self):
        self.assertEqual(markdown_to_blocks("    Hello\nI'm a block\n\nAnd I'm another one"), [
            "Hello\nI'm a block",
            "And I'm another one",
        ])

    def test_markdown_to_blocks_trailing_whitespace(self):
        self.assertEqual(markdown_to_blocks("Hello\nI'm a block    \n\nAnd I'm another one"), [
            "Hello\nI'm a block",
            "And I'm another one",
        ])

    def test_markdown_to_blocks_excessive_whitespace(self):
        self.assertEqual(markdown_to_blocks("\n\n\n\n\nBlock 1\nContinued\n\n\nBlock 2\n\n\n\n"), [
            "Block 1\nContinued",
            "Block 2",
        ])

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("Test"), "paragraph")
        self.assertEqual(block_to_block_type("Test\nTest"), "paragraph")

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Test"), "heading")
        self.assertEqual(block_to_block_type("###### Test"), "heading")

        self.assertEqual(block_to_block_type("#Test"), "paragraph")
        self.assertEqual(block_to_block_type("# "), "paragraph")
        self.assertEqual(block_to_block_type("####### Test"), "paragraph")
        self.assertEqual(block_to_block_type("# Test\nTest"), "paragraph")

    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type("```print('test')```"), "code")
        self.assertEqual(block_to_block_type("```\ndef main():\n\tprint('hello world')\n```"), "code")

        self.assertEqual(block_to_block_type("```print('test')``"), "paragraph")
        self.assertEqual(block_to_block_type("``print('test')```"), "paragraph")
        self.assertEqual(block_to_block_type("Test ```print('test')```"), "paragraph")
        self.assertEqual(block_to_block_type("```print('test')``` Test"), "paragraph")

    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type("> Test"), "quote")
        self.assertEqual(block_to_block_type("> Test\n> Test"), "quote")

        self.assertEqual(block_to_block_type(" >Test"), "paragraph")
        self.assertEqual(block_to_block_type("> Test\n>Test"), "paragraph")

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("* Test"), "unordered_list")
        self.assertEqual(block_to_block_type("* Test\n* Test"), "unordered_list")

        self.assertEqual(block_to_block_type("- Test"), "unordered_list")
        self.assertEqual(block_to_block_type("- Test\n- Test"), "unordered_list")

        self.assertEqual(block_to_block_type("- Test\n* Test"), "unordered_list")
        self.assertEqual(block_to_block_type("* Test\n- Test"), "unordered_list")

        self.assertEqual(block_to_block_type(" -Test"), "paragraph")
        self.assertEqual(block_to_block_type("- Test\n -Test"), "paragraph")

        self.assertEqual(block_to_block_type(" *Test"), "paragraph")
        self.assertEqual(block_to_block_type("* Test\n *Test"), "paragraph")

        self.assertEqual(block_to_block_type("-Test"), "paragraph")
        self.assertEqual(block_to_block_type("- Test\n-Test"), "paragraph")

        self.assertEqual(block_to_block_type("*Test"), "paragraph")
        self.assertEqual(block_to_block_type("* Test\n*Test"), "paragraph")

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1. Test"), "ordered_list")
        self.assertEqual(block_to_block_type("1. Test\n2. Test"), "ordered_list")

        self.assertEqual(block_to_block_type("2. Test"), "paragraph")
        self.assertEqual(block_to_block_type("1. Test\n1. Test"), "paragraph")

        self.assertEqual(block_to_block_type(" 1.Test"), "paragraph")
        self.assertEqual(block_to_block_type("1. Test\n 2.Test"), "paragraph")

        self.assertEqual(block_to_block_type("1.Test"), "paragraph")
        self.assertEqual(block_to_block_type("1.Test\n2.Test"), "paragraph")

    def test_markdown_to_html_node_paragraph(self):
        node = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "Hello world")
            ])
        ])
        self.assertEqual(markdown_to_html_node("Hello world"), node)

    def test_markdown_to_html_node_multiline_paragraph(self):
        node = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "Hello\nworld")
            ])
        ])
        self.assertEqual(markdown_to_html_node("Hello\nworld"), node)

    def test_markdown_to_html_node_multiple_paragraphs(self):
        block1 = "*Everyone* starts with **Hello World!**. In [Python](https://www.python.org/), this looks like `print('hello world')`"
        block2 = '![python logo](https://www.python.org/static/img/python-logo@2x.png)'
        node = ParentNode("div", [
            ParentNode("p", [
                LeafNode("i", "Everyone"),
                LeafNode(None, " starts with "),
                LeafNode("b", "Hello World!"),
                LeafNode(None, ". In "),
                LeafNode("a", "Python", props={"href": "https://www.python.org/"}),
                LeafNode(None, ", this looks like "),
                LeafNode("code", "print('hello world')")
            ]),
            ParentNode("p", [
                LeafNode("img", "", props={"src": "https://www.python.org/static/img/python-logo@2x.png", "alt": "python logo"})
            ])
        ])
        self.assertEqual(markdown_to_html_node(block1 + "\n\n" + block2), node)

    def test_markdown_to_html_node_quote(self):
        markdown = "> Hello world!\n> `print('hello world')`"
        node = ParentNode("div", [
            ParentNode("blockquote", [
                LeafNode(None, "Hello world!\n"),
                LeafNode("code", "print('hello world')")
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), node)

    def test_markdown_to_html_node_unordered_list(self):
        markdown = "* *First*\n* Second\n* Third and **final**"
        node = ParentNode("div", [
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode("i", "First"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "Second")
                ]),
                ParentNode("li", [
                    LeafNode(None, "Third and "),
                    LeafNode("b", "final")
                ])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), node)

    def test_markdown_to_html_node_ordered_list(self):
        markdown = "1. *First*\n2. Second\n3. Third and **final**"
        node = ParentNode("div", [
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode("i", "First"),
                ]),
                ParentNode("li", [
                    LeafNode(None, "Second")
                ]),
                ParentNode("li", [
                    LeafNode(None, "Third and "),
                    LeafNode("b", "final")
                ])
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), node)

    def test_markdown_to_html_node_code(self):
        markdown = "```\nif __name__ == '__main__':\n\tprint('hello world')\n```"
        node = ParentNode("div", [
            ParentNode("pre", [
                LeafNode("code", "if __name__ == '__main__':\n\tprint('hello world')")
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), node)

    def test_markdown_to_html_node_heading(self):
        markdown = "# Title\n\n## **Exciting** Introduction"
        node = ParentNode("div", [
            ParentNode("h1", [
                LeafNode(None, "Title")
            ]),
            ParentNode("h2", [
                LeafNode("b", "Exciting"),
                LeafNode(None, " Introduction")
            ])
        ])
        self.assertEqual(markdown_to_html_node(markdown), node)

    def test_extract_title(self):
        self.assertEqual(extract_title("# Title \n "), "Title")
        self.assertEqual(extract_title("# Multiline\nTitle"), "Multiline\nTitle")
        self.assertEqual(extract_title("# Title\n\n## Subtitle"), "Title")
        self.assertEqual(extract_title("# Title\n\nText"), "Title")

        with self.assertRaises(ValueError):
            extract_title("Title")
