import os
import shutil

def deploy():
    if os.path.exists("public"):
        shutil.rmtree("public")

    shutil.copytree("static", "public")

def main():
    deploy()

if __name__ == "__main__":
    main()
