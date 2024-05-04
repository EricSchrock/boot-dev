from htmlnode import HTMLNode
from textnode import TextNode

text = TextNode("Hello world", "bold", "example.com")
print(text)

a = HTMLNode(tag="a", value="link", props={"href": "https://example.com"})
p = HTMLNode(tag="p", value="hello", children=[a])
print(p)
print(a)
