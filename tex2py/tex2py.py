import re
from utils import rreplace

class TreeOfContents:
    """Tree abstraction for latex source"""

    __element = re.compile('(?P<name>[\S]+?)\{(?P<string>[\S\s]+?)\}')

    def __init__(self, tex='', branches=(), hierarchy=('section', 'subsection')):
        """Construct TreeOfContents object

        :param str name: name of latex element
        :param str string: content of latex element
        :param str tex: original tex
        :param list TreeOfContents branches: list of children
        :param list hierarchy: list of latex elements to determine hierarchy,
            which will otherwise be determined by latex syntax
        """
        self.tex = tex
        self.name, self.string = self.parseTag(tex)
        self.innerTex = self.stripTag(tex, self.name, self.string)
        self.branches = branches or self.parseBranches(self.innerTex)
        self.descendants = self.expandDescendants(self.branches)
        self.hierarchy = ('document',) + hierarchy

    @staticmethod
    def stripTag(tex, name, string):
        r"""Strip a tag from the provided tex

        >>> TOC.stripTag(
        ... '\\begin{itemize}\\item y\\end{itemize}', 'begin', 'itemize')
        '\\item y'
        """
        tag = '\\%s{%s}' % (name, string)
        stripped = tex.replace(tag, '', 1)
        if name == 'begin':
            tag = '\\%s{%s}' % ('end', string)
            stripped = rreplace(stripped, tag, '', 1)
        return stripped

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

    @staticmethod
    def parseBranches(tex):
        r"""
        Parse top level of provided latex

        >>> TOC.parseBranches('''
        ... \\section{Hello}
        ... This is some text.
        ... \\begin{enumerate}
        ... \\item Item!
        ... \\end{enumerate}
        ... \\section{Yolo}
        ... ''')
        """
        return []

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
        return TOC(tex)

TOC = TreeOfContents

if __name__ == '__main__':
    import doctest
    doctest.testmod()
