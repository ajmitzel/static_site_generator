from textnode import *
import re
from blocktype import *
from parentnode import ParentNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:

        extended_idx = 0
        if delimiter == "**":
            delimiter = r"\*\*"
            extended_idx = 1
        indices = [match.start() for match in re.finditer(delimiter , old_node.text)]


        num_of_new_nodes = len(indices)//2

        if num_of_new_nodes == 0:
            new_nodes.append(old_node)
        else:

            new_nodes.append(TextNode(old_node.text[0:indices[0]], TextType.TEXT))
            for i in range(0, len(indices), 2):
                new_nodes.append(TextNode(old_node.text[indices[i] + 1 + extended_idx: indices[i + 1]], text_type))
                if i >= len(indices) -2 :
                    new_nodes.append(TextNode(old_node.text[indices[i + 1] + 1 + extended_idx:], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(old_node.text[indices[i + 1] + 1 + extended_idx: indices[i + 2]], TextType.TEXT))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        indices = []
        lines = extract_markdown_images(node.text)

        if len(lines) == 0:
            new_nodes.append(node)
            continue
        for line in lines:
            indices.append(node.text.index(line[0]))

        if indices[0] != 0:
            new_nodes.append(TextNode(node.text[0:indices[0] - 2], TextType.TEXT))
        for idx in range(len(indices)):
            new_nodes.append(TextNode(node.text[indices[idx]:indices[idx] + len(lines[idx][0])], TextType.IMAGE, lines[idx][1]))

            if indices[idx] + len(lines[idx][0]) + len(lines[idx][1]) == len(node.text) - 3:
                return new_nodes
            else:
                if idx == len(indices) - 1:
                    new_nodes.append(TextNode(node.text[indices[idx] + len(lines[idx][0]) + len(lines[idx][1]) + 3:], TextType.TEXT))
                else: 
                    new_nodes.append(TextNode(node.text[indices[idx] + len(lines[idx][0]) + len(lines[idx][1]) + 3: indices[idx + 1]], TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        indices = []
        lines = extract_markdown_links(node.text)
        if len(lines) == 0:
            new_nodes.append(node)
            continue

        for line in lines:
            indices.append(node.text.index(line[0]))

        if indices[0] != 0:
            new_nodes.append(TextNode(node.text[0:indices[0] - 2], TextType.TEXT))
        for idx in range(len(indices)):
            new_nodes.append(TextNode(" " + node.text[indices[idx]:indices[idx] + len(lines[idx][0])], TextType.LINK, lines[idx][1]))

            if indices[idx] + len(lines[idx][0]) + len(lines[idx][1]) == len(node.text) - 3:
                return new_nodes
            else:
                if idx == len(indices) - 1:
                    new_nodes.append(TextNode(node.text[indices[idx] + len(lines[idx][0]) + len(lines[idx][1]) + 3:], TextType.TEXT))
                else: 
                    new_nodes.append(TextNode(node.text[indices[idx] + len(lines[idx][0]) + len(lines[idx][1]) + 3: indices[idx + 1] - 1], TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):

    raw_node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([raw_node], "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    for node in nodes:
        if node.text == None:
            nodes.remove(node)
    return nodes

def markdown_to_blocks(markdown):

    blocks = []

    raw_blocks = markdown.split('\n\n')
    for block in raw_blocks:
        if block == "":
            continue
        else:
            blocks.append(block.strip())
    return blocks

def markdown_to_html_node(markdown):
    converted_markdown = "<div>"
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        block_node = ParentNode(None, [], None)
        if block_type == BlockType.PARAGRAPH:
            block_node.tag = "p"
        elif block_type == BlockType.HEADING:
            block_node.tag = "h1"
            block = block[2:]
        elif block_type == BlockType.CODE:
            block_node.tag = "pre"
        elif block_type == BlockType.QUOTE:
            block_node.tag = "blockquote"
            block = block.replace(">", "\n").strip()
        elif block_type == BlockType.ORDERED_LIST:
            block_node.tag = "ol"
            list_items = re.findall(r"[1-9]\..+", block)
            new_block = ""
            for item in list_items:
                start_idx = block.index(item)
                new_item = "<li>" + block[start_idx + 3: start_idx + len(item)] + "</li>\n"
                new_block += new_item 
            block = new_block
        elif block_type == BlockType.UNORDERED_LIST:
            block_node.tag = "ul"
            list_items = re.findall(r"- .+", block)
            new_block = ""
            for item in list_items:
                start_idx = block.index(item)
                new_item = "<li>" + block[start_idx + 2: start_idx + len(item)] + "</li>\n"
                new_block += new_item 
            block = new_block
        else: 
            block_node.tag= "p"

        text_nodes = text_to_textnodes(block)
        if block_type == BlockType.CODE:
            block_node.children.append(LeafNode("code", block[3: len(block) - 3]))
        else:
            for node in text_nodes:
                block_node.children.append(text_node_to_html_node(node))
        converted_markdown += block_node.to_html()
    converted_markdown += "</div>"
    return converted_markdown

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line[0] == "#":
            return line[1:].strip()

    raise Exception("No header provided")

def generate_page(from_path, template_path, dest_path, root):
    print("Generating page from {} to {} using {}".format(from_path, dest_path, template_path))

    markdown_content = ""
    template_content = ""
    with open(from_path, 'r') as file:
        markdown_content = file.read()

    with open(template_path, 'r') as file:
        template_content = file.read()

    html_content = markdown_to_html_node(markdown_content)
    title = extract_title(markdown_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)
    template_content = template_content.replace("href=\"/", "href=\{}".format(root))

    dest = open(dest_path, "w")
    dest.write(template_content)
    dest.close()