import unittest
from inline_parser import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType

class test_inline_parser(unittest.TestCase):
    # split_nodes_delimiter
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

    # extract_markdown_images
    def test_extract_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), and here is ![another one](https://wallpapers.com/images/hd/beautiful-mountains-and-lake-2mpi93nx9sq4cot9.webp)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("another one", "https://wallpapers.com/images/hd/beautiful-mountains-and-lake-2mpi93nx9sq4cot9.webp")], matches)

    # extract_markdown_links
    def test_extract_link(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com)"
        )
        self.assertEqual([("link", "https://www.google.com")], matches)
    
    def test_extract_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.google.com), and then [another one](https://www.tacobell.com)"
        )
        self.assertEqual([("link", "https://www.google.com"), ("another one", "https://www.tacobell.com")], matches)
    
    def test_skip_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](www.tacobell.com)"
        )
        self.assertEqual([], matches)

    # split_nodes_image
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAINTEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAINTEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAINTEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_similar_words_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAINTEXT,
        )
        node2 = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAINTEXT,
        )
        new_nodes = split_nodes_image([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAINTEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAINTEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.PLAINTEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    # split_nodes_link
    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAINTEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAINTEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAINTEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_similar_words_link(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAINTEXT,
        )
        node2 = TextNode(
            "This is text with an ![imge](https://i.imgur.com/zjjcJKZ.png) and another [image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAINTEXT,
        )
        new_nodes = split_nodes_link([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAINTEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAINTEXT),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ![imge](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.PLAINTEXT),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )
    
    # text_to_textnodes
    def test_text_to_nodes(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
        self.assertEqual([
            TextNode("This is ", TextType.PLAINTEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAINTEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAINTEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAINTEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAINTEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], text_to_textnodes(text))
