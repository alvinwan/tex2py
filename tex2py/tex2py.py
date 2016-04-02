from texSoup import TexSoup

class TreeOfContents:
    """Tree abstraction for latex source"""

    source_type = TexSoup
    valid_tags = ('addcontentsline', 'addtocontents', 'addtocounter', 'address',
    'addtolength', 'addvspace', 'alph', 'appendix', 'arabic',
    'author', 'backslash', 'baselineskip', 'baselinestretch', 'bf', 'bibitem',
    'bigskipamount', 'bigskip', 'boldmath', 'boldsymbol', 'cal', 'caption',
    'cdots', 'centering', 'chapter', 'circle', 'cite', 'cleardoublepage',
    'clearpage', 'cline', 'closing', 'color', 'copyright', 'dashbox', 'date',
    'ddots', 'documentclass', 'dotfill', 'em', 'emph',
    'ensuremath (LaTeX2e)', 'epigraph', 'euro', 'fbox', 'flushbottom',
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
    'verb', 'vfill', 'vline', 'vphantom', 'vspace')
    allowed_attrs = ('string', 'name')
    default_hierarchy = ('section', 'subsection')

    def __init__(self, root, branches=(), descendants=(), source=None,
        depth=None, hierarchy=default_hierarchy):
        """
        Construct TreeOfContents object using source
        :param SourceType source: parsed source
        :param list TreeOfContents branches: list of direct children
        :param list SourceType descendants: all descendants
        :param list str hierarchy: list of latex elements to determine
            hierarchy, which will otherwise be determined by latex syntax
        """
        assert source is not None, 'NoneType source passed into TreeOfContents'
        self.source = source
        self.depth = depth or self.parseTopDepth()
        self.descendants = descendants or self.expandDescendants(branches)
        self.branches = branches or self.parseBranches(descendants)
        self.hierarchy = hierarchy

    @staticmethod
    def getHeadingLevel(ts, hierachy=default_hierarchy):
        """
        >>> ts = TexSoup('\\section{Hello}').section
        >>> TOC.getHeadingLevel(bs)
        0
        >>> ts2 = bsify('\\textbf{hello again}').textbf
        >>> TOC.getHeadingLevel(ts2)
        """
        try:
            return hierarchy.index(ts.name)+1
        except (ValueError, IndexError, TypeError):
            return None

    def parseTopDepth(self, hierarchy=None, form=r'\\%s'):
        """Parse tex for highest tag in hierarchy

        >>> TOC().parseTopTag('\\section{Hah}\\subsection{No}')
        'section'
        """
        hierarchy = hierarchy or self.hierarchy
        for i, command in enumerate(hierarchy + ('begin',), start=1):
            search = re.search(form % name, tex)
            if search: return i

    def expandDescendants(self, branches):
        """
        Expand descendants from list of branches
        :param list branches: list of immediate children as TreeOfContents objs
        :return: list of all descendants
        """
        return sum([b.descendants() for b in branches], []) + \
            [b.source for b in branches]

    def parseBranches(self, descendants):
        """
        Parse top level of latex
        :param list elements: list of source objects
        :return: list of filtered TreeOfContents objects
        """
        parsed, parent, cond = [], False, lambda b: (b.string or '').strip()
        for branch in filter(cond, descendants):
            if self.getHeadingLevel(branch) == self.depth:
                parsed.append({'root':branch.string, 'source':branch})
                parent = True
            elif not parent:
                parsed.append({'root':branch.string, 'source':branch})
            else:
                parsed[-1].setdefault('descendants', []).append(branch)
        return [TOC(depth=self.depth+1, **kwargs) for kwargs in parsed]

    def __getattr__(self, attr, *default):
        """Check source for attributes"""
        tag = attr[:-1]
        if attr in self.allowed_attrs:
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
    def fromLatex(tex):
        """Creates abstraction using Latex

        :param str tex: Latex
        :return: TreeOfContents object
        """
        return TOC('[document]', source=TexSoup.fromLatex(tex))
