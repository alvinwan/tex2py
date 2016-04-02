from .tex2py import TreeOfContents
from .texSoup import TexSoup


def tex2py(md, *args, **kwargs):
    """
    Converts latex file Python object

    :param str md: latex string
    :return: object
    """
    return TreeOfContents.fromLatex(md, *args, **kwargs)
