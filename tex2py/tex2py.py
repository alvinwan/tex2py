from TexSoup import TexSoup, TexNode

class TreeOfContents(object):
    """Tree abstraction for latex source"""

    source_type = TexNode
    valid_tags = ('addcontentsline', 'addtocontents', 'addtocounter', 'address',
    'addtolength', 'addvspace', 'alph', 'appendix', 'arabic',
    'author', 'backslash', 'baselineskip', 'baselinestretch', 'bf', 'bibitem',
    'bigskipamount', 'bigskip', 'boldmath', 'boldsymbol', 'cal', 'caption',
    'cdots', 'centering', 'chapter', 'circle', 'cite', 'cleardoublepage',
    'clearpage', 'cline', 'closing', 'color', 'copyright', 'dashbox', 'date',
    'ddots', 'documentclass', 'dotfill', 'em', 'emph',
    'ensuremath', 'epigraph', 'euro', 'fbox', 'flushbottom',
    'fnsymbol', 'footnote', 'footnotemark', 'footnotesize', 'footnotetext',
    'frac', 'frame', 'framebox', 'frenchspacing', 'hfill', 'hline', 'href',
    'hrulefill', 'hspace', 'huge', 'Huge', 'hyphenation', 'include',
    'includegraphics', 'includeonly', 'indent', 'input', 'it', 'item', 'kill',
    'label', 'large', 'Large', 'LARGE', 'LaTeX', 'LaTeXe', 'ldots', 'left',
    'lefteqn', 'line', 'linebreak', 'linethickness', 'linewidth',
    'listoffigures', 'listoftables', 'location', 'makebox', 'maketitle',
    'markboth markright', 'mathcal', 'mathop', 'mbox', 'medskip', 'multicolumn',
    'multiput', 'newcommand', 'newcolumntype', 'newcounter', 'newenvironment',
    'newfont', 'newlength', 'newline', 'newpage', 'newsavebox', 'newtheorem',
    'nocite', 'noindent', 'nolinebreak', 'nonfrenchspacing', 'normalsize',
    'nopagebreak', 'not', 'onecolumn', 'opening', 'oval', 'overbrace',
    'overline', 'pagebreak', 'pagenumbering', 'pageref', 'pagestyle', 'par',
    'paragraph', 'parbox', 'parindent', 'parskip', 'part', 'protect',
    'providecommand', 'put', 'quad', 'qquad', 'raggedbottom',
    'raggedleft', 'raggedright', 'raisebox', 'ref', 'renewcommand', 'right',
    'rm', 'roman', 'rule', 'savebox', 'sbox', 'sc', 'scriptsize', 'section',
    'setcounter', 'setlength', 'settowidth', 'sf', 'shortstack', 'signature',
    'sl', 'slash', 'small', 'smallskip', 'sout', 'space', 'sqrt', 'stackrel',
    'stepcounter', 'subparagraph', 'subsection', 'subsubsection',
    'tableofcontents', 'telephone', 'TeX', 'textbf', 'textcolor',
    'textit', 'textmd', 'textnormal', 'textrm', 'textsc', 'textsf',
    'textsl', 'texttt', 'textup', 'textwidth', 'textheight', 'thanks',
    'thispagestyle', 'tiny', 'title', 'today', 'tt', 'twocolumn', 'typeout',
    'typein', 'uline', 'underbrace', 'underline', 'unitlength', 'usebox',
    'usecounter', 'uwave', 'value', 'vbox', 'vcenter', 'vdots', 'vector',
    'verb', 'vfill', 'vline', 'vphantom', 'vspace', 'document')
    allowed_attrs = ('string', 'name')
    default_hierarchy = ('chapter', 'section', 'subsection')

    def __init__(self, root, branches=(), descendants=(), source=None,
        depth=None, hierarchy=()):
        """Construct TreeOfContents object using source

        :param TexNode source: parsed source
        :param list TreeOfContents branches: list of direct children
        :param list TexNode descendants: all descendants
        :param list str hierarchy: list of latex elements to determine
            hierarchy, which will otherwise be determined by latex syntax
        """
        super().__init__()
        assert source is not None, 'NoneType source passed into TreeOfContents'
        self.source = source
        self.root = root
        self.hierarchy = hierarchy or self.findHierarchy()
        self.depth = depth or self.parseTopDepth()-1
        self.branches = branches or self.parseBranches(descendants)
        self.descendants = descendants or self.expandDescendants(self.branches)

    def findHierarchy(self, max_subs=10):
        """Find hierarchy for the LaTeX source.

        >>> TOC.fromLatex(r'\subsection{yo}\section{hello}').findHierarchy()
        ('section', 'subsection')
        >>> TOC.fromLatex(
        ... r'\subsubsubsection{huh}\subsubsection{hah}').findHierarchy()
        ('subsubsection', 'subsubsubsection')
        >>> TOC.fromLatex('\section{h1}\subsection{subh1}\section{h2}\
        ... \subsection{subh2}').findHierarchy()
        ('section', 'subsection')
        """
        hierarchy = []
        defaults = TOC.default_hierarchy + tuple(
            '%ssection' % ('sub'*i) for i in range(2, max_subs))
        for level in defaults:
            if getattr(self.source, level):
                hierarchy.append(level)
        return tuple(hierarchy)

    @staticmethod
    def getHeadingLevel(ts, hierarchy=default_hierarchy):
        """Extract heading level for a particular Tex element, given a specified
        hierarchy.

        >>> ts = TexSoup(r'\section{Hello}').section
        >>> TOC.getHeadingLevel(ts)
        2
        >>> ts2 = TexSoup(r'\chapter{hello again}').chapter
        >>> TOC.getHeadingLevel(ts2)
        1
        >>> ts3 = TexSoup(r'\subsubsubsubsection{Hello}').subsubsubsubsection
        >>> TOC.getHeadingLevel(ts3)
        6
        """
        try:
            return hierarchy.index(ts.name)+1
        except ValueError:
            if ts.name.endswith('section'):
                i, name = 0, ts.name
                while name.startswith('sub'):
                    name, i = name[3:], i+1
                if name == 'section':
                    return i+2
            return float('inf')
        except (AttributeError, TypeError):
            return float('inf')

    def parseTopDepth(self, descendants=()):
        """Parse tex for highest tag in hierarchy

        >>> TOC.fromLatex('\\section{Hah}\\subsection{No}').parseTopDepth()
        1
        >>> s = '\\subsubsubsection{Yo}\\subsubsection{Hah}'
        >>> TOC.fromLatex(s).parseTopDepth()
        1
        >>> h = ('section', 'subsubsection', 'subsubsubsection')
        >>> TOC.fromLatex(s, hierarchy=h).parseTopDepth()
        2
        """
        descendants = list(descendants) or \
            list(getattr(self.source, 'descendants', descendants))
        if not descendants:
            return -1
        return min(TOC.getHeadingLevel(e, self.hierarchy) for e in descendants)

    def expandDescendants(self, branches=None):
        """
        Expand descendants from list of branches
        :param list branches: list of immediate children as TreeOfContents objs
        :return: list of all descendants

        >>> toc = TOC.fromLatex(r'\section{h1}\subsection{subh1}\section{h2}\
        ... \subsection{subh2}')
        >>> len(list(toc.source.descendants))
        8
        >>> len(toc.descendants)
        8
        """
        branches = branches or self.branches
        return sum([b.descendants for b in branches], []) + \
            [b.source for b in branches]

    def parseBranches(self, descendants):
        """
        Parse top level of latex
        :param list elements: list of source objects
        :return: list of filtered TreeOfContents objects

        >>> toc = TOC.fromLatex(r'\section{h1}\subsection{subh1}\section{h2}\
        ... \subsection{subh2}')
        >>> toc.parseTopDepth(toc.descendants)
        1
        >>> toc.parseBranches(toc.descendants)
        [h1, h2]
        >>> len(toc.branches)
        2
        >>> len(toc.section.branches)
        1
        """
        strfy = lambda s: s if isinstance(s, str) else s.string
        i, branches = self.parseTopDepth(descendants), []
        for descendant in descendants:
            if self.getHeadingLevel(descendant, self.hierarchy) == i:
                branches.append({'source': descendant})
            if self.getHeadingLevel(descendant, self.hierarchy) > i \
                and branches:
                branches[-1].setdefault('descendants', []).append(descendant)
        return [TOC(strfy(descendant), depth=i, hierarchy=self.hierarchy,
            **branch) for branch in branches]

    def __getattr__(self, attr, *default):
        """Check source for attributes"""
        tag = attr[:-1]
        if attr in self.allowed_attrs:
            if isinstance(self.source, str):
                return self.source
            return getattr(self.source, attr, *default)
        if attr in self.valid_tags:
            return next(filter(lambda t: t.name == attr, self.branches), None)
        if len(default):
            return default[0]
        if attr[-1] == 's' and tag in self.valid_tags:
            condition = lambda t: t.name == tag
            return filter(condition, self.branches)
        raise AttributeError("'TreeOfContents' object has no attribute '%s'" % attr)

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
    def fromLatex(tex, *args, **kwargs):
        """Creates abstraction using Latex

        :param str tex: Latex
        :return: TreeOfContents object
        """
        source = TexSoup(tex)
        return TOC('[document]', source=source,
            descendants=list(source.descendants), *args, **kwargs)

TOC = TreeOfContents
