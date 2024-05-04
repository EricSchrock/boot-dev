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
        repr = f"tag: {self.tag} | value: {self.value} | props: {self.props_to_html()} | children:"

        if self.children:
            for child in self.children:
                repr += f" {child.tag}"

        return repr
