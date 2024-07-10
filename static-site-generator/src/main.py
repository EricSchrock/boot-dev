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

def generate_pages_recursive(content_dir_path: str, template_path: str, dest_dir_path: str):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for item in os.listdir(content_dir_path):
        if os.path.isfile(f"{content_dir_path}/{item}"):
            generate_page(f"{content_dir_path}/{item}", template_path, f"{dest_dir_path}/{item.replace(".md", ".html")}")
        else:
            generate_pages_recursive(f"{content_dir_path}/{item}", template_path, f"{dest_dir_path}/{item}")

def main():
    deploy()
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
