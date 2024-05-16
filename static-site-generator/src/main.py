from textnode import TextNode

node = TextNode("Test a **bold** new *feature* involving `code`", "text")

nodes = node.split('**')

splits = []
for node in nodes:
    splits.extend(node.split('*'))

nodes = []
for split in splits:
    nodes.extend(split.split('`'))

for node in nodes:
    print(node)
