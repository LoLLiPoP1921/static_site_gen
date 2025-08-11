import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()
