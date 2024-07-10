import re
from typing import List

from htmlnode import LeafNode, ParentNode
from textnode import TextNode

def markdown_to_blocks(markdown: str) -> List[str]:
    return [ block.strip() for block in markdown.split("\n\n") if block not in  ["", "\n"]]

def block_to_block_type(block: str) -> str:
    if re.match(r"#{1,6} [^\n]+\Z", block):
        return "heading"

    if re.match(r"```(.|\n)*```\Z", block):
        return "code"

    lines = block.split('\n')

    if all([ line[0] == '>' for line in lines ]):
        return "quote"

    if all([ line.startswith("* ") or line.startswith("- ") for line in lines ]):
        return "unordered_list"

    if all([ line.startswith(f"{i}. ") for line, i in zip(lines, range(1, len(lines)+1)) ]):
        return "ordered_list"

    return "paragraph"

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        if block_to_block_type(block) == "paragraph":
            tag = "p"
            grandchildren = paragraph_to_html_node(block)

        children.append(ParentNode(tag, grandchildren))

    return ParentNode("div", children)

def paragraph_to_html_node(block: str) -> List[LeafNode]:
    nodes = TextNode(block, "text").split()
    return [ node.to_html_node() for node in nodes ]
