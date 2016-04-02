from tex2py import tex2py, TreeOfContents

chikin = open('tests/samples/chikin.tex').read()
iscream = open('tests/samples/iscream.tex').read()

tocs2strs = lambda tocs: list(map(str, tocs))

##############
# MAIN TESTS #
##############

def test_basic_prop():
    """tests that custom __getattr__ works"""
    toc = tex2py(chikin)
    assert str(toc) == ''
    assert toc.depth == 1
    assert len(toc.branches) == 1
    assert isinstance(toc.section, TreeOfContents)

def test_get_tags():
    """tests that tags are printed correctly"""
    toc = tex2py(chikin)

    assert len(list(toc.sections)) == 1
    assert str(toc.section) == repr(toc.section) == toc.section.string == 'Chikin Tales'

def test_top_level():
    """tests parse for the top level of a markdown string"""
    toc = tex2py(chikin)

    assert str(toc.section) == 'Chikin Tales'
    assert len(list(toc.subsections)) == 0
    assert toc.depth == 1

def test_top_level2():
    """tests parse for top level of markdown string with only subsections"""
    toc = tex2py(iscream)

    assert toc.section is None
    assert str(toc.subsection) == 'I Scream'
    assert len(list(toc.subsections)) == 2
    assert toc.depth == 2

def test_indexing():
    """test indices"""
    toc = tex2py(chikin)

    assert list(toc.section.subsections)[1] == toc.section[1]
    assert str(toc.section[1]) == 'Chikin Scream'

def test_branches_limit():
    """Tests that branches include only headings of higher depth"""
    toc = tex2py(chikin)

    assert toc.section.subsection.string == 'Chikin Fly'
