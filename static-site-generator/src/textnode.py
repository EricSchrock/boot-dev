from htmlnode import LeafNode
from typing import List, Self

class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None):
        if not text_type in ["text", "bold", "italic", "code", "link", "image"]:
            raise ValueError(f"text_type={text_type} is invalid")

        if not url and text_type in ["link", "image"]:
            raise ValueError(f"text_type={text_type} requires a url")

        if url and text_type not in ["link", "image"]:
            raise ValueError(f"text_type={text_type} does not include a url")

        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_html_node(self) -> LeafNode:
        if self.text_type == "text":
            return LeafNode(value=self.text)
        if self.text_type == "bold":
            return LeafNode(tag="b", value=self.text)
        if self.text_type == "italic":
            return LeafNode(tag="i", value=self.text)
        if self.text_type == "code":
            return LeafNode(tag="code", value=self.text)
        if self.text_type == "link":
            return LeafNode(tag="a", value=self.text, props={"href": self.url})
        if self.text_type == "image":
            return LeafNode(tag="img", value="", props={"src": self.url, "alt": self.text})
        raise ValueError("unsupported node type")

    def split(self, delimiter: str) -> List[Self]:
        if self.text_type != "text":
            return [self]

        types = {'**': 'bold', '*': "italic", '`': "code"}

        if delimiter not in types.keys():
            raise ValueError(f"delimiter={delimiter} is invalid")

        splits = self.text.split(delimiter)
        if len(splits) % 2 == 0:
            raise ValueError(f"unpaired {delimiter} delimiter (syntax error)")

        nodes = []
        types = ["text", types[delimiter]]
        while len(splits) > 0:
            index = 1 if len(splits) % 2 == 0 else 0
            text = splits.pop(0)
            if not text:
                continue

            nodes.append(TextNode(text, types[index]))

        return nodes

