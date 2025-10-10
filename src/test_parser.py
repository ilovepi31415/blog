import unittest
from parser import split_nodes_delimiter
from textnode import TextNode, TextType

class test_parser(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.PLAINTEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAINTEXT),
        ])
    
    def test_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", TextType.PLAINTEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.PLAINTEXT),
        ])

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.PLAINTEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.PLAINTEXT),
        ])
    
    def test_multiple_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAINTEXT)
        node2 = TextNode("This is a second bit of text with a `code block` word", TextType.PLAINTEXT)
        node3 = TextNode("This is text with `multiple` blocks of `code` inside of `it`", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node, node2, node3], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.PLAINTEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAINTEXT),
            TextNode("This is a second bit of text with a ", TextType.PLAINTEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAINTEXT),
            TextNode("This is text with ", TextType.PLAINTEXT),
            TextNode("multiple", TextType.CODE),
            TextNode(" blocks of ", TextType.PLAINTEXT),
            TextNode("code", TextType.CODE),
            TextNode(" inside of ", TextType.PLAINTEXT),
            TextNode("it", TextType.CODE),
        ])
    
    def test_multiple_types(self):
        node = TextNode("This is _text_ with **many** types of `inline` sections", TextType.PLAINTEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAINTEXT),
            TextNode("text", TextType.ITALIC),
            TextNode(" with ", TextType.PLAINTEXT),
            TextNode("many", TextType.BOLD),
            TextNode(" types of ", TextType.PLAINTEXT),
            TextNode("inline", TextType.CODE),
            TextNode(" sections", TextType.PLAINTEXT),
        ])