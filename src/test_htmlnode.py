import unittest
from htmlnode import HTMLNode, LeafNode

class test_HTMLNode(unittest.TestCase):
    def test_defaults(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_props(self):
        node = HTMLNode(props={'href': 'www.google.com', 'target': '_blank'})
        self.assertEqual(node.props_to_html(), 'href="www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode('a', 'test-value', None, {'class': 'small'})
        self.assertEqual(node.__repr__(), 'HTMLNode(a, test-value, None, {\'class\': \'small\'})')
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_props(self):
        node = LeafNode('a', 'clicky clicky', {'href': 'www.google.com'})
        self.assertEqual(node.to_html(), '<a href="www.google.com">clicky clicky</a>')
    
    def test_leaf_to_html_invalid(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)