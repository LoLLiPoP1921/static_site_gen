from Leafnode import LeafNode
from textnode import TextNode, TextType

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    tt = text_node.text_type
    txt = text_node.text
    url = text_node.url

    if tt == TextType.PLAIN:
        return LeafNode(None, txt)

    if tt == TextType.BOLD:
        return LeafNode("b", txt)

    if tt == TextType.ITALIC:
        return LeafNode("i", txt)

    if tt == TextType.LINK:
        if not url:
            raise ValueError("LINK TextNode requires a url")
        return LeafNode("a", txt, {"href": url})

    raise ValueError(f"Unsupported TextType: {tt}")