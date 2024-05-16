from textnode import TextNode

node = TextNode("Text with ![two](https://example.com) ![images](https://example.com) and also a [couple](https://example.com) [links](https://example.com)", "text")

print(node.extract_images())
print(node.extract_links())
