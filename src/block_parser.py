from enum import Enum
import re

class BlockType(Enum):
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    ULIST = 'ul'
    OLIST = 'ol'
    PARAGRAPH = 'p'

def markdown_to_blocks(markdown: str):
    """
    Split markdown text into blocks at double newlines
    """
    blocks = []
    sections = markdown.split('\n\n')
    for section in sections:
        # Remove blank sections
        section = section.strip()
        if section:
            blocks.append(section)
    return blocks

def block_to_block_type(block: str):
    """
    Find the BlockType of a block of text
    """
    # If the line starts with 1-6 #'s it is a heading 
    if re.findall(r'^#{1,6}', block.strip('\n')):
        return BlockType.HEADING
    
    # A codeblock starts and ends with triple backticks '```'
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    
    # The other types must be true for all lines
    lines = block.split('\n')
    maybe_quote, maybe_ul, maybe_ol = True, True, True
    for line in lines:
        # If one lines fails the test, it cannot be that BlockType
        if not line:
            continue
        if not line.startswith('>'):
            # All quote lines must start with '>'
            maybe_quote = False
        if not line.startswith('- '):
            # All unordered list lines must start with '- '
            maybe_ul = False
        if not re.findall(r'^\d+\. ', line):
            # All ordered list lines must start with a number 'n. '
            maybe_ol = False
    if maybe_quote:
        return BlockType.QUOTE
    if maybe_ul:
        return BlockType.ULIST
    if maybe_ol:
        return BlockType.OLIST
    
    # Default to a paragraph
    return BlockType.PARAGRAPH

