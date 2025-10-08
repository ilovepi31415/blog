import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is another node", TextType.PLAINTEXT)
        self.assertNotEqual(node, node2)
    
    def test_url(self):
        node = TextNode('test', TextType.LINK, None)
        node2 = TextNode('test', TextType.LINK)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAINTEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, 'www.google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {'href': 'www.google.com'})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, 'static/test.png')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'image')
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {'src': 'static/test.png', 'alt': 'This is an image node'})

if __name__ == '__main__':
    unittest.main()