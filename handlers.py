# Handlers
# Handlers responsible for generating the resulting marked-up text
# after receiving detailed instructions from the Parser.

#Notes:
# 
class Handler(object):
    """ Object that handles method calls from the Parser.

    The Parser will call start() and end() methods at the beginning
    of each block, with the proper block name as a parameter. The 
    sub() mehtod will be used in reg expression substituion. 
    When called with a name such as 'emphasis', it will return 
    a proper substituion function. """

    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if callable(method): 
            return method(*args)

    def start(self, name):
        self.callback('start_', name)
    def end(self, name):
        self.callback('end_', name)
    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None: match.group(0)
            return result
        return substitution


class HTMLRenderer(Handler):
    """ A specific handler used for rendering HTML

    The methods are accessed from the superclass Handler's start(),
    end(), and sub() methods. They implement basic markup as used in 
    HTML documents."""
    def start_document(self):
        print '<html><head><title>...</title></head></html>'
    
    def end_document(self):
        print '</body></html>'

    def start_paragraph(self):
        print '<p>'
    def end_paragraph(self):
        print '</p>'

    def start_heading(self):
        print '<h2>'
    def end_heading(self):
        print '</h2>'
    def start_list(self):
        print '<ul>'
    def end_list(self):
        print '</ul>'
    def start_listitem(self):
        print '<li>'
    def end_listitem(self):
        print '</li>'
    def start_title(self):
        print '<h1>'
    def end_title(self):
        print '</h1>'
    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)
    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))
    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))
    def feed(self, data):
        print data