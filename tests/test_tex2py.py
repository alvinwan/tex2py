from tex2py import tex2py, TreeOfContents
from TexSoup import TexSoup
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
    assert str(chikin) == '[document]' == chikin.name
    assert chikin.depth == 0
    assert len(chikin.branches) == 2
    assert isinstance(chikin.section, TreeOfContents)

def test_get_tags(chikin):
    """tests that tags are printed correctly"""
    assert len(list(chikin.sections)) == 2
    assert str(chikin.section) == repr(chikin.section) == chikin.section.string == 'Chikin Tales'

def test_top_level(chikin):
    """tests parse for the top level of a markdown string"""
    assert str(chikin.section) == 'Chikin Tales'
    assert len(list(chikin.subsections)) == 0

def test_top_level2(iscream):
    """tests parse for top level of markdown string with only subsections"""
    assert iscream.section is None
    assert len(iscream.branches) == 2
    assert str(iscream.subsection) == 'I Scream'
    assert len(list(iscream.subsections)) == 2
    assert iscream.depth == 0

def test_level_depth(chikin):
    """Test that depth is correct"""
    assert chikin.depth == 0
    assert str(chikin.section) == 'Chikin Tales'
    assert chikin.section.depth == 1
    assert chikin.section.subsection.depth == 2

def test_indexing(chikin):
    """test indices"""
    assert list(chikin.section.subsections)[0] == chikin.section[0]
    assert str(chikin.section[0]) == 'Chikin Fly'

def test_branches_limit(chikin):
    """Tests that branches include only headings of higher depth"""
    assert chikin.section.subsection.string == 'Chikin Fly'

#################
# UTILITY TESTS #
#################

def test_nested_descendants(chikin):
    """Test nested descendants."""
    assert len(chikin.section.descendants) == 3
    assert chikin.section.parseTopDepth(chikin.section.descendants) == 2
    assert len(chikin.section.branches) == 1
    assert str(chikin.section.subsection) == 'Chikin Fly'

def test_find_hierarchy(chikin):
    """Tests that hierarchy is identified correctly"""
    hie = chikin.findHierarchy()
    assert hie == ('section', 'subsection')
    assert chikin.depth == 0
    section = TexSoup(r'\section{asdf}').section
    assert chikin.getHeadingLevel(section, hie) == 1
    assert chikin.parseTopDepth(chikin.descendants) == 1
