import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list[str], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        original_type = node.text_type
        segments = node.text.split(delimiter)
        for i in range(len(segments)):
            segment = segments[i]
            if not segment:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(segment, original_type))
            else:
                new_nodes.append(TextNode(segment, text_type))
    return new_nodes

def extract_markdown_images(text: str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extarct_markdown_links(text: str):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
