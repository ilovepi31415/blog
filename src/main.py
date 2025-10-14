from textnode import TextType, TextNode
from htmlnode import HTMLNode
from markdown_to_html import markdown_to_html_node
import os, shutil, sys

def copy_tree(src: str, dest: str):
    if (
        not os.path.exists(src) or 
        not os.path.isdir(src) or
        (os.path.exists(dest) and not os.path.isdir(dest))):
        raise Exception('invalid source or destination path')
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    for path in os.listdir(src):
        if os.path.isfile(os.path.join(src, path)):
            shutil.copy(os.path.join(src, path), dest)
        else:
            os.mkdir(os.path.join(dest, path))
            copy_tree(os.path.join(src, path), os.path.join(dest, path))
            
def extract_title(markdown: str):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith('# '):
            title = line[1:].strip()
            if title:
                return title
    raise Exception('No title in file')

def generate_page(from_path, template_path, dest_path, basepath):
    if (
        not os.path.exists(from_path) or 
        os.path.isdir(from_path) or
        os.path.isdir(dest_path) or
        not os.path.exists(template_path) or
        os.path.isdir(template_path)
        ):
        raise Exception('invalid source or destination path') 
    print(from_path, template_path, dest_path)
    with open(from_path, 'r') as f:
        content = f.read()
    with open(template_path, 'r') as t:
        template = t.read()
    html = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    new_text = template.replace('{{ Title }}', title).replace('{{ Content }}', html)
    new_text = new_text.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    with open(dest_path, 'w') as d:
        d.write(new_text)

def generate_page_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    for path in os.listdir(dir_path_content):
        if path.endswith('.md'):
            generate_page(os.path.join(dir_path_content, path), template_path, os.path.join(dest_dir_path, path)[:-2] + 'html', basepath)
        else:
            os.makedirs(os.path.join(dest_dir_path, path), exist_ok=True)
            generate_page_recursively(os.path.join(dir_path_content, path), template_path, os.path.join(dest_dir_path, path), basepath)


def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = '/'
    copy_tree('static', 'docs')
    generate_page_recursively('content', 'template.html', 'docs', basepath)

main()