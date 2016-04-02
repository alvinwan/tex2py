from .tex2py import TreeOfContents


def tex2py(md, *args, **kwargs):
    """
    Converts latex file Python object

    :param str md: latex string
    :return: object
    """
    return TreeOfContents.fromLatex(md, *args, **kwargs)
