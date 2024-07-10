import re
from typing import List

from htmlnode import ParentNode
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
            children.append(paragraph_to_html_node(block))
        elif block_to_block_type(block) == "quote":
            children.append(quote_to_html_node(block))
        elif block_to_block_type(block) == "unordered_list":
            children.append(unordered_list_to_html_node(block))
        elif block_to_block_type(block) == "ordered_list":
            children.append(ordered_list_to_html_node(block))

    return ParentNode("div", children)

def paragraph_to_html_node(block: str) -> ParentNode:
    nodes = [ node.to_html_node() for node in TextNode(block, "text").split() ]
    return ParentNode("p", nodes)

def quote_to_html_node(block: str) -> ParentNode:
    block = block.replace("\n>", "\n")[1:]
    nodes = [ node.to_html_node() for node in TextNode(block, "text").split() ]
    return ParentNode("blockquote", nodes)

def unordered_list_to_html_node(block: str) -> ParentNode:
    nodes = []
    for line in block.split("\n"):
        nodes.append(ParentNode("li", [ node.to_html_node() for node in TextNode(line[2:], "text").split()]))
    return ParentNode("ul", nodes)

def ordered_list_to_html_node(block: str) -> ParentNode:
    nodes = []
    for line in block.split("\n"):
        nodes.append(ParentNode("li", [ node.to_html_node() for node in TextNode(line.split(". ")[1], "text").split()]))
    return ParentNode("ol", nodes)
