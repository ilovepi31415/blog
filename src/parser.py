import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        segments = node.text.split(delimiter)
        for i in range(len(segments)):
            segment = segments[i]
            if not segment:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(segment, node.text_type, node.url))
            else:
                new_nodes.append(TextNode(segment, text_type))
    return new_nodes

def extract_markdown_images(text: str):
    return re.findall(r"\!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        segments = [node.text]
        matches = extract_markdown_images(node.text)
        for match in matches:
            bad_string = f'![{match[0]}]({match[1]})'
            new_segments = segments[-1].split(bad_string, 1)
            segments = segments[:-1] + new_segments
        for i in range(len(segments) - 1):
            if segments[i]:
                new_nodes.append(TextNode(segments[i], node.text_type, node.url))
            new_nodes.append(TextNode(matches[i][0], TextType.IMAGE, matches[i][1]))
        if segments[-1]:
            new_nodes.append(TextNode(segments[-1], node.text_type, node.url))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for node in old_nodes:
        segments = [node.text]
        matches = extract_markdown_links(node.text)
        for match in matches:
            bad_string = f'[{match[0]}]({match[1]})'
            start_index = 0
            new_segments = segments[-1].split(bad_string, 1)
            segments = segments[:-1] + new_segments
        for i in range(len(segments) - 1):
            if segments[i]:
                new_nodes.append(TextNode(segments[i], node.text_type, node.url))
            if i < len(matches):
                new_nodes.append(TextNode(matches[i][0], TextType.LINK, matches[i][1]))
        if segments[-1]:
            new_nodes.append(TextNode(segments[-1], node.text_type, node.url))
    return new_nodes

def text_to_textnodes(text: str):
    initial_node = TextNode(text, TextType.PLAINTEXT)
    new_nodes = split_nodes_image([initial_node])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    return new_nodes