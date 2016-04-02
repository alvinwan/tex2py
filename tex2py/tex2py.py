import re
from utils import rreplace

class TreeOfContents:
    """Tree abstraction for latex source"""

    __element = re.compile('(?P<name>[\S]+?)\{(?P<string>[\S\s]+?)\}')

    def __init__(self, tex='', name=None, string=None, branches=(),
        hierarchy=('section', 'subsection')):
        """Construct TreeOfContents object

        :param str name: name of latex element
        :param str string: content of latex element
        :param str tex: original tex
        :param list TreeOfContents branches: list of children
        :param list str hierarchy: list of latex elements to determine
            hierarchy, which will otherwise be determined by latex syntax
        """
        if name:
            self.name, self.string = name, string
        else:
            self.name, self.string = self.parseTag(tex)

        self.tex = tex
        self.innerTex = self.stripTag(tex, self.name, self.string)
        self.branches = branches or self.parseBranches(self.innerTex)
        self.descendants = self.expandDescendants(self.branches)
        self.hierarchy = hierarchy + ('begin',)

    @staticmethod
    def stripTag(tex, name, string, form='\\%s{%s}'):
        r"""Strip a tag from the provided tex, only from the beginning and end.

        >>> TOC.stripTag('\\begin{b}\\item y\\end{b}', 'begin', 'b')
        '\\item y'
        >>> TOC.stripTag('\\begin{b}\\begin{b}\\item y\\end{b}\\end{b}',
        ... 'begin', 'b')
        '\\begin{b}\\item y\\end{b}'
        """
        stripped = tex.replace(form % (name, string), '', 1)
        if name == 'begin':
            stripped = rreplace(stripped, form % ('end', string), '', 1)
        return stripped

    def parseTopTag(tex, hierarchy=None, form=r'\\%s\{(?P<string>[\S\s]+?\})'):
        """Parse tex for highest tag in hierarchy"""
        hierarchy = hierarchy or self.hierarchy
        for name in hierarchy:
            search = re.search(form % name)
            if search:
                return name, search.group('string')
        return '[text]', tex  # Warning: [text] is not an actual tag name

    @staticmethod
    def parseNameString(tex):
        r"""Extract name of latex element from tex

        >>> TOC.parseNameString('\\textbf{hello}\\textbf{yolo}')
        ('\\textbf', 'hello')
        """
        match = re.search(TOC.__element, tex)
        if not match:
            return '', ''
        return match.group('name'), match.group('string')

    @staticmethod
    def expandDescendants(branches):
        """Expand descendants from list of branches

        :param list branches: list of immediate children as TreeOfContents objs
        :return: list of all descendants
        """
        return sum([b.descendants() for b in branches], []) + branches

    def parseBranches(self, tex, hierarchy=None):
        r"""
        Parse top level of provided latex

        >>> TOC().parseBranches('''
        ... \\section{Hello}
        ... This is some text.
        ... \\begin{enumerate}
        ... \\item Item!
        ... \\end{enumerate}
        ... \\section{Yolo}
        ... ''')
        """
        hierarchy = hierarchy or self.hierarchy
        tag = self.parseTopTag(tex, hierarchy)

    def __getattr__(self, attr, *default):
        """Check source for attributes"""
        pass

    def __repr__(self):
        """Display contents"""
        return str(self)

    def __str__(self):
        """Display contents"""
        return self.string

    def __iter__(self):
        """Iterator over children"""
        return iter(self.branches)

    def __getitem__(self, i):
        return self.branches[i]

    @staticmethod
    def fromFile(path):
        """Creates abstraction using path to file

        :param str path: path to tex file
        :return: TreeOfContents object
        """
        return TOC.fromLatex(open(path).read())

    @staticmethod
    def fromLatex(tex):
        """Creates abstraction using Latex

        :param str tex: Latex
        :return: TreeOfContents object
        """
        if tex.strip().startswith('\\begin{document}'):
            return TOC(tex)
        return TOC(tex, name='[document]', string='')

TOC = TreeOfContents

if __name__ == '__main__':
    import doctest
    doctest.testmod()
