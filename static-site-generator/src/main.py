from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode

print("\nTextNode examples\n----------")
nodes = []
nodes.append(TextNode("Test", "text"))
nodes.append(TextNode("Test", "bold"))
nodes.append(TextNode("Test", "italic"))
nodes.append(TextNode("Test", "code"))
nodes.append(TextNode("Test", "link", "https://example.com"))
nodes.append(TextNode("Test", "image", "https://example.com"))
for node in nodes:
    print(node)

print()
print("Convert TextNodes to LeafNodes\n----------")
for node in nodes:
    print(node.to_html_node())

print()
print("HTMLNode examples\n----------")
html1 = HTMLNode(tag="a", value="link", props={"href": "https://example.com"})
html2 = HTMLNode(tag="p", value="hello", children=[html1])
print(html1)
print(html2)

print()
print("LeafNode examples\n----------")
leaf1 = LeafNode(tag="a", value="link", props={"href": "https://example.com"})
leaf2 = LeafNode(tag="p", value="hello")
print(leaf1)
print(leaf2)

print()
print("ParentNode examples\n----------")
parent1 = ParentNode(tag="p", children=[leaf1])
parent2 = ParentNode(tag="p", children=[parent1, leaf2])
print(parent1)
print(parent2)
