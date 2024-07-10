import os
import shutil

from markdown import extract_title, markdown_to_html_node

def deploy():
    if os.path.exists("public"):
        shutil.rmtree("public")

    shutil.copytree("static", "public")

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        markdown = f.read()

    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()

    with open(template_path, 'r') as f:
        page = f.read()

    page = page.replace("{{ Title }}", title).replace("{{ Content }}", content)

    with open(dest_path, 'w') as f:
        f.write(page)

def main():
    deploy()
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()
