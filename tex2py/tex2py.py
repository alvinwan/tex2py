class TreeOfContents:
    """Tree abstraction for markdown source"""


    def __init__(self, string, branches=()):
        """
        Construct TreeOfContents object using source

        :param
        :param list TreeOfContents branches: list of direct children
        """
        self.string = string
        self.branches = branches

    def expandDescendants(self, branches):
        """
        Expand descendants from list of branches

        :param list branches: list of immediate children as TreeOfContents objs
        :return: list of all descendants
        """
        return sum([b.descendants() for b in branches], []) + branches

    def parseBranches(self, descendants):
        """
        Parse top level of markdown

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
        """
        Creates abstraction using path to file

        :param str path: path to tex file
        :return: TreeOfContents object
        """
        return TOC.fromLatex(open(path).read())

    @staticmethod
    def fromLatex(tex):
        """
        Creates abstraction using Latex

        :param str tex: Latex
        :return: TreeOfContents object
        """
        return TOC('', tex)

TOC = TreeOfContents
