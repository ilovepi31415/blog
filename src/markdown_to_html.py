from block_parser import BlockType, block_to_block_type, markdown_to_blocks
from inline_parser import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode
import re

def markdown_to_html_node(markdown: str):
    """
    Converts a markdown file into a tree of HTML nodes with a single parent
    """
    # Convert to blocks
    blocks = markdown_to_blocks(markdown)
    # Deal with each block
    nodes = blocks_to_text_nodes(blocks)
    # Makes blocks children of a div
    return ParentNode('div', nodes)

def blocks_to_text_nodes(blocks: list[str]):
    """
    Converts a list of markdown blocks into TextNodes using helper functions for each BlockType
    """
    block_nodes = []
    for block in blocks:
        # Find each block's BlockType and use the appropriate helper function
        block_type = block_to_block_type(block)
        match(block_type):
            case BlockType.CODE:
                block_nodes.append(code_to_html_node(block))
            case BlockType.OLIST:
                block_nodes.append(ol_to_html_node(block))
            case BlockType.ULIST:
                block_nodes.append(ul_to_html_node(block))
            case BlockType.QUOTE:
                block_nodes.append(quote_to_html_node(block))
            case BlockType.PARAGRAPH:
                block_nodes.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                block_nodes.append(heading_to_html_node(block))
    return block_nodes

def code_to_html_node(block_text: str):
    """
    Convert a codeblock into a TextNode
    """
    # Remove the bookending backticks
    block_text = block_text.strip('```')
    block_text = block_text[1:] # Remove the leading \n for some reason
    code_node = TextNode(block_text, TextType.CODE)
    return ParentNode('pre', [text_node_to_html_node(code_node)])

def ol_to_html_node(block_text: str):
    """
    Convert an ordered list into a TextNode
    """
    # Add the list item HTML tags to each line
    lines = block_text.split('\n')
    for i in range(len(lines)):
        lines[i] = '<li>' + re.sub(r'^\d+\. ', '', lines[i]) + '</li>'
    block_text = ''.join(lines)
    return ParentNode('ol', text_to_children(block_text))

def ul_to_html_node(block_text: str):
    """
    Convert an unordered list into a TextNode
    """
    # Add the list item HTML tags to each line
    lines = block_text.split('\n')
    for i in range(len(lines)):
        lines[i] = '<li>' + re.sub(r'^- ', '', lines[i]) + '</li>'
    block_text = ''.join(lines)
    return ParentNode('ul', text_to_children(block_text))

def quote_to_html_node(block_text: str):
    """
    Convert a quoteblock into a TextNode
    """
    # Remove the '>' from the beginning of each line and combine the leftover text
    lines = block_text.split('\n')
    for i in range(len(lines)):
        lines[i] = re.sub(r'^>', '', lines[i]).strip()
    block_text = '\n'.join(lines)
    return ParentNode('blockquote', text_to_children(block_text))

def paragraph_to_html_node(block_text: str):
    """
    Convert a paragraph into a TextNode
    """
    # Remove all extra newlines from the paragraph
    block_text = block_text.replace('\n', ' ')
    return ParentNode('p', text_to_children(block_text))

def heading_to_html_node(block_text: str):
    """
    Convert a heading into a TextNode
    """
    # Use the number of #'s to determine the heading number
    heading, body = block_text.split(' ', 1)
    return ParentNode(f'h{len(heading)}', text_to_children(body))

def text_to_children(text: str):
    """
    Convert the text within a BlockNode into a list of inline HTMLNodes
    """
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes