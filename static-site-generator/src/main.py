from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode

def text_node_to_html_node(node: TextNode):
    if node.text_type == "text":
        return LeafNode(value=node.text)
    if node.text_type == "bold":
        return LeafNode(tag="b", value=node.text)
    if node.text_type == "italic":
        return LeafNode(tag="i", value=node.text)
    if node.text_type == "code":
        return LeafNode(tag="code", value=node.text)
    if node.text_type == "link":
        return LeafNode(tag="a", value=node.text, props={"href": node.url})
    if node.text_type == "image":
        return LeafNode(tag="img", value="", props={"src": node.url, "alt": node.text})
    raise ValueError("Unsupported node type")

print("\nTextNode examples")
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
print("Convert TextNodes to LeafNodes")
for node in nodes:
    print(text_node_to_html_node(node))

print()
print("HTMLNode examples")
html1 = HTMLNode(tag="a", value="link", props={"href": "https://example.com"})
html2 = HTMLNode(tag="p", value="hello", children=[html1])
print(html1)
print(html2)

print()
print("LeafNode examples")
leaf1 = LeafNode(tag="a", value="link", props={"href": "https://example.com"})
leaf2 = LeafNode(tag="p", value="hello")
print(leaf1)
print(leaf2)

print()
print("ParentNode examples")
parent1 = ParentNode(tag="p", children=[leaf1])
parent2 = ParentNode(tag="p", children=[parent1, leaf2])
print(parent1)
print(parent2)
