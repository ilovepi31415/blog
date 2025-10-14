from textnode import TextType, TextNode
from htmlnode import HTMLNode
import os, shutil

def copy_tree(src: str, dest: str):
    if (
        not os.path.exists(src) or 
        not os.path.exists(dest) or
        not os.path.isdir(src) or
        not os.path.isdir(dest)):
        raise Exception('invalid source or destination path')
    shutil.rmtree(dest)
    os.mkdir(dest)
    for path in os.listdir(src):
        print(path)
        if os.path.isfile(os.path.join(src, path)):
            shutil.copy(os.path.join(src, path), dest)
        else:
            os.mkdir(os.path.join(dest, path))
            copy_tree(os.path.join(src, path), os.path.join(dest, path))
            

def main():
    node = TextNode('hello world', TextType.PLAINTEXT, 'www.tacobell.com')
    print(node)
    copy_tree('static', 'public')

main()