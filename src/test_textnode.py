import unittest

from textnode import TextNode, TextType
from HTMLnode import HTMLNode
from Leafnode import LeafNode
from ParentNode import ParentNode
from text_node_to_html_node import text_node_to_html_node
from SplitNodesDelimiter import split_nodes_delimiter
from extract_markdown import extract_markdown_images, extract_markdown_links


class TestTextNode(unittest.TestCase):
    def test_eq_same_values(self):
        n1 = TextNode("This is a text node", TextType.BOLD)
        n2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(n1, n2)

    def test_default_url_is_none(self):
        n = TextNode("hello", TextType.PLAIN)
        self.assertIsNone(n.url)

    def test_not_equal_different_text(self):
        n1 = TextNode("hello", TextType.PLAIN)
        n2 = TextNode("HELLO", TextType.PLAIN)
        self.assertNotEqual(n1, n2)

    def test_not_equal_different_type(self):
        n1 = TextNode("hello", TextType.BOLD)
        n2 = TextNode("hello", TextType.ITALIC)
        self.assertNotEqual(n1, n2)

    def test_not_equal_different_url(self):
        n1 = TextNode("click", TextType.LINK, "https://a.com")
        n2 = TextNode("click", TextType.LINK, "https://b.com")
        self.assertNotEqual(n1, n2)

    def test_eq_when_both_urls_none(self):
        n1 = TextNode("x", TextType.UNDERLINE, None)
        n2 = TextNode("x", TextType.UNDERLINE, None)
        self.assertEqual(n1, n2)

    def test_repr_format(self):
        n = TextNode("click", TextType.LINK, "https://example.com")
        self.assertEqual(
            repr(n),
            "TextNode('click', TextType.LINK, 'https://example.com')",
        )

    def test_not_equal_with_non_textnode(self):
        n = TextNode("x", TextType.PLAIN)
        self.assertFalse(n == "x")  # __eq__ should return False

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        node = HTMLNode(
            "a",
            "Google",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "hello", props={})
        self.assertEqual(node.props_to_html(), "")
        node2 = HTMLNode("p", "hello", props=None)
        self.assertEqual(node2.props_to_html(), "")

    def test_children_default_list(self):
        node = HTMLNode("div", None)
        self.assertIsInstance(node.children, list)
        self.assertEqual(node.children, [])

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "hi")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr_has_fields(self):
        node = HTMLNode("a", "x", props={"href": "u"})
        s = repr(node)
        self.assertIn("HTMLNode(", s)
        self.assertIn("tag='a'", s)
        self.assertIn("value='x'", s)
        self.assertIn("props", s)

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_no_tag_raw_text(self):
        node = LeafNode(None, "just text")
        self.assertEqual(node.to_html(), "just text")

    def test_leaf_raises_without_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

    def test_leaf_has_no_children(self):
        node = LeafNode("span", "x")
        self.assertEqual(node.children, [])  # leaf nodes don't keep children

class TestParentNode(unittest.TestCase):
    def test_parent_with_children(self):
        child1 = LeafNode("b", "Bold")
        child2 = LeafNode(None, " and ")
        child3 = LeafNode("i", "italic")
        parent = ParentNode("p", [child1, child2, child3])
        self.assertEqual(
            parent.to_html(),
            "<p><b>Bold</b> and <i>italic</i></p>"
        )

    def test_parent_with_props(self):
        child = LeafNode(None, "Click here")
        parent = ParentNode("a", [child], {"href": "https://google.com"})
        self.assertEqual(
            parent.to_html(),
            '<a href="https://google.com">Click here</a>'
        )

    def test_parent_without_tag_raises(self):
        child = LeafNode("span", "oops")
        with self.assertRaises(ValueError):
            ParentNode(None, [child])

    def test_parent_without_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)

class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        n = TextNode("This is a text node", TextType.PLAIN)
        hn = text_node_to_html_node(n)
        self.assertIsNone(hn.tag)
        self.assertEqual(hn.value, "This is a text node")

    def test_bold(self):
        n = TextNode("Bold", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(n).to_html(), "<b>Bold</b>")

    def test_italic(self):
        n = TextNode("It", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(n).to_html(), "<i>It</i>")

    def test_link(self):
        n = TextNode("Click", TextType.LINK, "https://ex.com")
        self.assertEqual(
            text_node_to_html_node(n).to_html(),
            '<a href="https://ex.com">Click</a>'
        )

    def test_unsupported_raises(self):
        with self.assertRaises(ValueError):
            class Dummy: pass
            # Fake type to force the error
            n = TextNode("x", TextType("unknown"))  # or monkeypatch if needed

class TestSplitNodes(unittest.TestCase):
    def test_code_backticks(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        out = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("This is text with a ", TextType.PLAIN),
             ("code block", TextType.CODE),
             (" word", TextType.PLAIN)]
        )

    def test_bold_double_asterisks(self):
        node = TextNode("a **bold** move and **more**", TextType.PLAIN)
        out = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("a ", TextType.PLAIN),
             ("bold", TextType.BOLD),
             (" move and ", TextType.PLAIN),
             ("more", TextType.BOLD)]
        )

    def test_italic_single_underscore(self):
        node = TextNode("mix _it_ up", TextType.PLAIN)
        out = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            [(n.text, n.text_type) for n in out],
            [("mix ", TextType.PLAIN),
             ("it", TextType.ITALIC),
             (" up", TextType.PLAIN)]
        )

    def test_non_text_nodes_pass_through(self):
        n1 = TextNode("plain", TextType.PLAIN)
        n2 = TextNode("link", TextType.LINK, url="https://x.y")
        out = split_nodes_delimiter([n1, n2], "`", TextType.CODE)
        self.assertEqual(out[1], n2)  # unchanged

    def test_unbalanced_raises(self):
        node = TextNode("oops `no close", TextType.PLAIN)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

class TestExtractMarkdown(unittest.TestCase):

    # --- IMAGE TESTS ---
    def test_extract_single_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "![one](https://img.com/1.png) and ![two](https://img.com/2.jpg)"
        matches = extract_markdown_images(text)
        self.assertListEqual([
            ("one", "https://img.com/1.png"),
            ("two", "https://img.com/2.jpg")
        ], matches)

    def test_extract_no_images(self):
        text = "This is text without images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    # --- LINK TESTS ---
    def test_extract_single_link(self):
        text = "This is a [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_multiple_links(self):
        text = "[google](https://google.com) and [github](https://github.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("google", "https://google.com"),
            ("github", "https://github.com")
        ], matches)

    def test_extract_no_links(self):
        text = "This is text without links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_link_and_image_mixed(self):
        text = "Here is [a link](https://site.com) and ![an image](https://img.com/img.png)"
        link_matches = extract_markdown_links(text)
        img_matches = extract_markdown_images(text)

        self.assertListEqual([("a link", "https://site.com")], link_matches)
        self.assertListEqual([("an image", "https://img.com/img.png")], img_matches)
        
if __name__ == "__main__":
    unittest.main()
