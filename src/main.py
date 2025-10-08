from textnode import TextType, TextNode
from htmlnode import HTMLNode

def main():
    node = TextNode('hello world', TextType.PLAINTEXT, 'www.tacobell.com')
    print(node)

main()