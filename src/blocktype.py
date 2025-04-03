import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    heading_pattern = r"#{1,6} "
    code_pattern = r"```[\w\W]*```"
    ordered_list_pattern = r"^[1-9]\. "

    if re.search(heading_pattern, block) != None:
        return BlockType.HEADING

    elif re.search(code_pattern, block) != None:
        return BlockType.CODE
    
    else:
        if block[0] == ">":
            for line in block.split("\n"):
                if line[0] != ">":
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        elif block[0:2] == "- ":
            for line in block.split("\n"):
                if line[0:2] != "- ":
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST

        elif re.search(ordered_list_pattern, block) != None:
            for line in block.split("\n"):
                if re.search(ordered_list_pattern, line) == None:
                    return BlockType.PARAGRAPH
            return BlockType.ORDERED_LIST
        
        return BlockType.PARAGRAPH

    