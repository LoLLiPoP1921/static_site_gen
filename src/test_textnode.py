import unittest

from textnode import TextNode, TextType
from HTMLnode import HTMLNode


class TestTextNode(unittest.TestCase):

    #textnode.py
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

    
    # HTMLnode.py
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

if __name__ == "__main__":
    unittest.main()
