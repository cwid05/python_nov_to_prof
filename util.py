# Util

def lines(file):
    for line in file: yield line
    yield '\n'

def blocks(file):
    """
    Creates blocks from text lines with out an empty row between (paragraphs).
    ->If line is not blank, then append to block.
    ->Once you hit a blank, yield the joined contents and create a new blank block 
    to keep iterating through the lines in the file.
    """
    block = []
    for line in lines(file):
        if line.strip():
            block.append(line)
        elif block:
            print repr(block)  #print only for illustrative purposes
            yield ''.join(block).strip()
            block = []