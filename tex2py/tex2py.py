import re

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
        self.name, self.string = self.parseNameString(tex)
        self.branches = branches or self.parseBranches(tex)
        self.hierarchy = ('document',) + hierarchy

    def parseNameString(self, tex):
        """Extract name of latex element from tex

        >>> hello = TOC('\\\\textbf{hello}')
        >>> hello.name
        '\\\\textbf'
        >>> hello.string
        'hello'
        >>> hello
        hello
        """
        match = re.search(self.__element, tex)
        if not match:
            return '', ''
        return match.group('name'), match.group('string')

    def parseTopDepth(self):
        """Parse highest level in tex"""
        pass

    def expandDescendants(self, branches):
        """Expand descendants from list of branches

        :param list branches: list of immediate children as TreeOfContents objs
        :return: list of all descendants
        """
        return sum([b.descendants() for b in branches], []) + branches

    def parseBranches(self, descendants):
        """
        Parse top level of latex

        :param list elements: list of objects
        :return: list of filtered TreeOfContents objects
        """
        pass

    def __getattr__(self, attr, *default):
        """Check source for attributes"""
        pass

    def __repr__(self):
        """Display contents"""
        return str(self)

    def __str__(self):
        """Display contents"""
        return self.string or ''

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
