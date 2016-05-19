from tex2py.tex2py import TreeOfContents
from TexSoup import TexSoup


def tex2py(tex, *args, **kwargs):
    """
    Converts latex file Python object

    :param str tex: latex string
    :return: object
    """
    return TreeOfContents.fromLatex(tex, *args, **kwargs)
