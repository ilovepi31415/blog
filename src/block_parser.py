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
    blocks = []
    sections = markdown.split('\n\n')
    for section in sections:
        section = section.strip()
        if section:
            blocks.append(section)
    return blocks

def block_to_block_type(block: str):
    if re.findall(r'^#{1,6}', block.strip('\n')):
        return BlockType.HEADING
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    lines = block.split('\n')
    maybe_quote, maybe_ul, maybe_ol = True, True, True
    for line in lines:
        if not line:
            continue
        if not line.startswith('>'):
            maybe_quote = False
        if not line.startswith('- '):
            maybe_ul = False
        if not re.findall(r'^\d+\. ', line):
            maybe_ol = False
    if maybe_quote:
        return BlockType.QUOTE
    if maybe_ul:
        return BlockType.ULIST
    if maybe_ol:
        return BlockType.OLIST
    return BlockType.PARAGRAPH

