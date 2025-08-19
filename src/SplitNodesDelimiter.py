from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        # Odd number of parts means a balanced delimiter count (0,2,4,... delimiters)
        if len(parts) % 2 == 0:
            raise ValueError("Unbalanced delimiter in text: missing closing delimiter")

        for i, chunk in enumerate(parts):
            if chunk == "":
                # Skip empty chunks (e.g., text like "``" or "**")
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(chunk, TextType.PLAIN))
            else:
                new_nodes.append(TextNode(chunk, text_type))
    return new_nodes