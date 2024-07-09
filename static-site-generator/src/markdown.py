import re
from typing import List

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

    if all([ line[0] in ['*', '-'] for line in lines ]):
        return "unordered_list"

    if all([ (line[0] == str(i) and line[1] == '.') for line, i in zip(lines, range(1, len(lines)+1)) ]):
        return "ordered_list"

    return "paragraph"
