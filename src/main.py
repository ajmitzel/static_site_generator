from textnode import *
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from processing_functions import *
from blocktype import block_to_block_type
import os 
import shutil

def index_into_directory(base_path, destination_folder, base_folder, convert_to_html):

    tree_path = []
    curr_dir = os.listdir(base_path)

    new_path = ""
    for d in curr_dir:
        curr_path = "{}/{}".format(base_path, d)
        if os.path.isfile(curr_path):
            if convert_to_html and curr_path[len(curr_path) - 3: len(curr_path)] == ".md":
                print("this triggered")
                new_file = d.replace(".md", ".html")
                generate_page(curr_path, "template.html", "{}/{}".format(destination_folder, new_file))
            else:
                new_path = shutil.copy(curr_path, "{}/".format(destination_folder))
            tree_path.append(new_path)
        else:
            os.mkdir("{}/{}".format(destination_folder, d))
            tree_path.extend(index_into_directory(curr_path, "{}/{}".format(destination_folder, d), d, convert_to_html))
    return tree_path

def main():
    
    dirs = os.listdir("public/")

    for d in dirs:
        curr_path = "public/{}".format(d)
        if os.path.isfile(curr_path):
            os.remove(curr_path)
        else:
            shutil.rmtree(curr_path)
    
    tree_path = index_into_directory("static", "public", "", True)
    test_tree_path = index_into_directory("content", "public", "", True)



main()

