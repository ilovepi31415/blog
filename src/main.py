from textnode import TextType, TextNode

def main():
    node = TextNode('hello world', TextType.PLAINTEXT, 'www.tacobell.com')
    print(node)

main()