# LaTeX2Python (tex2py)

[![Build Status](https://travis-ci.org/alvinwan/tex2py.svg?branch=master)](https://travis-ci.org/alvinwan/tex2py)
[![Coverage Status](https://coveralls.io/repos/github/alvinwan/tex2py/badge.svg?branch=master)](https://coveralls.io/github/alvinwan/tex2py?branch=master)

Tex2py converts LaTeX into a Python parse tree, using [TexSoup](http://github.com/alvinwan/texsoup). This allows you to
navigate latex files as trees, using either the default or a custom hierarchy. See [md2py](https://github.com/alvinwan/md2py) for a markdown parse tree.

> Note `tex2py` currently only supports Python3.

created by [Alvin Wan](http://alvinwan.com)

# Installation

Install via pip.

```
pip install tex2py
```

# Usage

LaTeX2Python offers only one function `tex2py`, which generates a Python
parse tree from Latex. This object is a navigable, "Tree of Contents"
abstraction for the latex file.

Take, for example, the following latex file. ([See pdf](https://github.com/alvinwan/tex2py/blob/master/tests/samples/chikin.pdf))

**chikin.tex**

```
\documentclass[a4paper]{article}
\begin{document}

\section{Chikin Tales}

\subsection{Chikin Fly}

Chickens don't fly. They do only the following:

\begin{itemize}
\item waddle
\item plop
\end{itemize}

\section{Chikin Scream}

\subsection{Plopping}

Plopping involves three steps:

\begin{enumerate}
\item squawk
\item plop
\item repeat, unless ordered to squat
\end{enumerate}

\subsection{I Scream}

\end{document}
```

Akin to a navigation bar, the `TreeOfContents` object allows you to expand a
latex file one level at a time. Running `tex2py` on the above latex file
will generate a tree, abstracting the below structure.

```
          <Document>
          /        \
  Chikin Tales   Chikin Scream
      /            /     \
 Chikin Fly  Plopping   I Scream
```

At the global level, we can access the title.

```
>>> from tex2py import tex2py
>>> with open('chikin.tex') as f: data = f.read()
>>> toc = tex2py(data)
>>> toc.section
Chikin Tales
>>> str(toc.section)
'Chikin Tales'
```

Notice that at this level, there are no `subsection`s.

```
>>> list(toc.subsections)
[]
```

The main `section` has two `subsection`s beneath it. We can access both.

```
>>> list(toc.section.subsections)
[Chikin Fly, Chikin Scream]
>>> toc.section.subsection
Chikin Fly
```

The `TreeOfContents` class also has a few more conveniences defined. Among them
is support for indexing. To access the `i`th child of an `<element>` - instead of `<element>.branches[i]` - use `<element>[i]`.

See below for example usage.

```
>>> toc.section.branches[0] == toc.section[0] == toc.section.subsection
True
>>> list(toc.section.subsections)[1] == toc.section[1]
True
>>> toc.section[1]
Chikin Scream
```

You can now print the document tree. (There is some weirdness with branches beyond titles, so for only titles, we have the following:

```
           ┌Chikin Tales┐
           │            └Chikin Fly
 [document]┤
           │             ┌Plopping
           └Chikin Scream┤
                         │        
                         │        
                         └I Scream
```

# Additional Notes

- Behind the scenes, tex2py uses [`TexSoup`](https://github.com/alvinwan/TexSoup). All tex2py objects have a
`source` attribute containing a [TexSoup](https://github.com/alvinwan/TexSoup) object.
