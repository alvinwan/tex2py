from tex2py import tex2py, TreeOfContents
import pytest

tocs2strs = lambda tocs: list(map(str, tocs))

@pytest.fixture(scope='function')
def chikin():
    """Instance of the chikin tex file"""
    return tex2py(open('tests/samples/chikin.tex').read())

@pytest.fixture(scope='function')
def iscream():
    """Instance of the iscream tex file"""
    return tex2py(open('tests/samples/iscream.tex').read())

##############
# MAIN TESTS #
##############

def test_basic_prop(chikin):
    """tests that custom __getattr__ works"""
    assert str(chikin) == ''
    assert chikin.depth == 1
    assert len(chikin.branches) == 1
    assert isinstance(chikin.section, TreeOfContents)

def test_get_tags(chikin):
    """tests that tags are printed correctly"""
    assert len(list(chikin.sections)) == 2
    assert str(chikin.section) == repr(chikin.section) == chikin.section.string == 'Chikin Tales'

def test_top_level(chikin):
    """tests parse for the top level of a markdown string"""
    assert str(chikin.section) == 'Chikin Tales'
    assert len(list(chikin.subsections)) == 0
    assert chikin.depth == 1

def test_top_level2(iscream):
    """tests parse for top level of markdown string with only subsections"""
    assert iscream.section is None
    assert str(iscream.subsection) == 'I Scream'
    assert len(list(iscream.subsections)) == 2
    assert iscream.depth == 2

def test_indexing(chikin):
    """test indices"""
    assert list(chikin.section.subsections)[1] == toc.section[1]
    assert str(chikin.section[1]) == 'Chikin Scream'

def test_branches_limit(chikin):
    """Tests that branches include only headings of higher depth"""
    assert chikin.section.subsection.string == 'Chikin Fly'
