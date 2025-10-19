import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    """
    Splits TextNodes into other TextTypes at a given delimiter

    Parameters:
    old_nodes -- the original list of TextNodes
    delimiter -- the string at which to separate nodes
    text_type -- the TextType that should be given to text within the delimiter
    """
    new_nodes = []

    # Handle each node in the old_nodes list
    for node in old_nodes:
        # Split the node at the delimiter
        segments = node.text.split(delimiter)
        for i in range(len(segments)):
            # Change nodes within the delimiter to the new TextType
            # Since nodes are split at every delimiter, nodes alternate from inside to outside
            segment = segments[i]
            if not segment: # Prevents blank nodes from being added
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(segment, node.text_type, node.url))
            else:
                new_nodes.append(TextNode(segment, text_type))
    return new_nodes

def extract_markdown_images(text: str):
    """
    Find all instances of a markdown image within text
    Format: ![text](link)
    """
    return re.findall(r"\!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text: str):
    """
    Find all instances of a markdown link within text
    Format: [alt_text](image_link)
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    """
    Separates TextNodes at images and returns a new list of TextNodes
    """
    new_nodes = []
    for node in old_nodes:
        # Start an array of segments with the node text
        segments = [node.text]
        matches = extract_markdown_images(node.text)

        # Remove all image text and split the Node at those points
        for match in matches:
            bad_string = f'![{match[0]}]({match[1]})'
            new_segments = segments[-1].split(bad_string, 1)
            segments = segments[:-1] + new_segments

        # Build the Nodes back with text and image Nodes
        for i in range(len(segments) - 1):
            if segments[i]: # Prevent blank TextNodes
                # Add the section of text
                new_nodes.append(TextNode(segments[i], node.text_type, node.url))
            if i < len(matches):
                # Add the image
                new_nodes.append(TextNode(matches[i][0], TextType.IMAGE, matches[i][1]))
        if segments[-1]:
            new_nodes.append(TextNode(segments[-1], node.text_type, node.url))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]):
    """
    Separates TextNodes at links and returns a new list of TextNodes
    """
    new_nodes = []
    for node in old_nodes:
        # Start an array of segments with the node text
        segments = [node.text]
        matches = extract_markdown_links(node.text)

        # Remove all link text and split the Node at those points
        for match in matches:
            bad_string = f'[{match[0]}]({match[1]})'
            new_segments = segments[-1].split(bad_string, 1)
            segments = segments[:-1] + new_segments

        # Build the Nodes back with text and link Nodes
        for i in range(len(segments) - 1):
            if segments[i]:
                # Add the section of text
                new_nodes.append(TextNode(segments[i], node.text_type, node.url))
            if i < len(matches):
                # Add the image
                new_nodes.append(TextNode(matches[i][0], TextType.LINK, matches[i][1]))
        if segments[-1]:
            new_nodes.append(TextNode(segments[-1], node.text_type, node.url))
    return new_nodes

def text_to_textnodes(text: str):
    """
    Combine all the above functions to convert markdown text into a list of TextNodes with images, links, and other TextTypes
    """
    initial_node = TextNode(text, TextType.PLAINTEXT)
    new_nodes = split_nodes_image([initial_node])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    return new_nodes