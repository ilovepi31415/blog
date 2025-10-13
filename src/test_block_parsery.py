import unittest
from block_parser import BlockType, markdown_to_blocks, block_to_block_type

class test_block_parser(unittest.TestCase):
    # markdown_to_blocks
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_extra_whitespace(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line






- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
           blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    # block_to_block_type
    def test_heading(self):
        text = '''
### heading
'''
        self.assertEqual(block_to_block_type(text), BlockType.HEADING)

    def test_code(self):
        text = '```code in here la la la```'
        self.assertEqual(block_to_block_type(text), BlockType.CODE)
    
    def test_quote(self):
        text = '''
>This is a quote
>This is more quote
>So much quote
'''
        self.assertEqual(block_to_block_type(text), BlockType.QUOTE)
    
    def test_ul(self):
        text = '''
- list thing
- more list things
- so many llist things
'''
        self.assertEqual(block_to_block_type(text), BlockType.ULIST)
    
    def test_ol(self):
        text = '''
1. First thing
2. Second thing
10000. Why so many things?
'''
        self.assertEqual(block_to_block_type(text), BlockType.OLIST)
    
    def test_paragraph(self):
        text = '''
 # Not a heading
> not a quote
'''
        self.assertEqual(block_to_block_type(text), BlockType.PARAGRAPH)