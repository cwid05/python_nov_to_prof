# markup.py main file
# Parser- uses a handler and set of rules and filters to transform 
# plain-text file into a marked-up file (this case in HTML). 
# Needs: 
#     - a constructor to set things up,
#     - a method to add rules,
#     - a method to add filters,
#     - and a method to parse a given file

import sys, re
from handlers import *
from util import *
from rules import *

class Parser(object):
    """
    A parser reads a text file, applying rules and controlling a handler.
    """
    def __init__(self, handler):
        self.handler = handler            #assigns supplied handler to instance
        self.rules = []
        self.filters = []

    def addRule(self, rule):
        """ Adds a rule to rule list"""
        self.rules.append(rule)

    def addFilter(self, pattern, name):
        """ Creates the filter, then adds to filter list.
        Filter is a function that applies re.sub with appropriate reg exp
        and uses a replacement from the handler accessed with handler.sub(name)
        """
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')
        for block in blocks(file):
            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):          # All rules have a condition method
                    last = rule.action(block, self.handler)
                    if last: break
        self.handler.end('document')

class BasicTextParser(Parser):
    """
    A specific Parser that adds rules and filters in its constructor.
    """
    def __init__(self, handler):
        Parser.__init__(self, handler)
        self.addRule(ListRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'(http://[\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')

handler = HTMLRenderer()
parser = BasicTextParser(handler)

parser.parse(sys.stdin)
