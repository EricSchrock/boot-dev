from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode

text = TextNode("Hello world", "bold", "example.com")
print(text)

html1 = HTMLNode(tag="a", value="link", props={"href": "https://example.com"})
print(html1)

html2 = HTMLNode(tag="p", value="hello", children=[html1])
print(html2)

leaf1 = LeafNode(tag="a", value="link", props={"href": "https://example.com"})
print(leaf1)

leaf2 = LeafNode(tag="p", value="hello")
print(leaf2)

parent1 = ParentNode(tag="p", children=[leaf1])
print(parent1)

parent2 = ParentNode(tag="p", children=[parent1, leaf2])
print(parent2)
