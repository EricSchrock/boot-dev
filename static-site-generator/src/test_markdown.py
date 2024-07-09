import unittest

from markdown import markdown_to_blocks, block_to_block_type

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
        self.assertEqual(block_to_block_type(">Test"), "quote")
        self.assertEqual(block_to_block_type(">Test\n>Test"), "quote")

        self.assertEqual(block_to_block_type(" >Test"), "paragraph")
        self.assertEqual(block_to_block_type(">Test\n >Test"), "paragraph")

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("*Test"), "unordered_list")
        self.assertEqual(block_to_block_type("*Test\n*Test"), "unordered_list")

        self.assertEqual(block_to_block_type("-Test"), "unordered_list")
        self.assertEqual(block_to_block_type("-Test\n-Test"), "unordered_list")

        self.assertEqual(block_to_block_type("-Test\n*Test"), "unordered_list")
        self.assertEqual(block_to_block_type("*Test\n-Test"), "unordered_list")

        self.assertEqual(block_to_block_type(" -Test"), "paragraph")
        self.assertEqual(block_to_block_type("-Test\n -Test"), "paragraph")

        self.assertEqual(block_to_block_type(" *Test"), "paragraph")
        self.assertEqual(block_to_block_type("*Test\n *Test"), "paragraph")

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1.Test"), "ordered_list")
        self.assertEqual(block_to_block_type("1.Test\n2.Test"), "ordered_list")

        self.assertEqual(block_to_block_type("2.Test"), "paragraph")
        self.assertEqual(block_to_block_type("1.Test\n1.Test"), "paragraph")

        self.assertEqual(block_to_block_type(" 1.Test"), "paragraph")
        self.assertEqual(block_to_block_type("1.Test\n 2.Test"), "paragraph")
