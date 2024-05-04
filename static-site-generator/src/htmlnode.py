from typing import Dict, List, Self

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: List[Self] = None, props: Dict[str, str] = None):
        if not value and not children:
            raise RuntimeError("value and children cannot both be None")

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        html = ""
        for k, v in self.props.items():
            html += f' {k}="{v}"'
        return html

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, props: Dict[str, str] = None):
        if not value:
            raise ValueError("value must be set")

        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        if not self.tag:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
