from textnode import *
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from processing_functions import *
from blocktype import block_to_block_type
import os 
import shutil

def index_into_directory(base_path, destination_folder, base_folder):

    tree_path = []
    curr_dir = os.listdir(base_path)
    new_path = ""
    for d in curr_dir:
        if os.path.isfile("{}/{}".format(base_path, d)):
            new_path = shutil.copy("{}/{}".format(base_path, d), "{}/{}".format(destination_folder, base_folder))
            tree_path.append(new_path)
        else:
            os.mkdir("{}/{}".format(destination_folder, d))
            tree_path.append(index_into_directory("{}/{}".format(base_path, d), "{}/{}".format(destination_folder, base_folder), d))
    return tree_path

def main():
    
    dirs = os.listdir("public/")

    for d in dirs:
        curr_path = "public/{}".format(d)
        if os.path.isfile(curr_path):
            os.remove(curr_path)
        else:
            shutil.rmtree(curr_path)
    
    tree_path = index_into_directory("static", "public", "")
    generate_page("content/index.md", "template.html", "public/index.html")


main()

