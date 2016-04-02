# LaTeX2Python (tex2py)

tex2py converts LaTeX into a Python parse tree. This allows you to
navigate a latex file as a document structure.

See [md2py](https://github.com/alvinwan/md2py) for a markdown parse tree.

## Usage

> **Differences From md2py** Note that tex2py mirrors BeautifulSoup's approach
to a document tree. In many ways, it thus differs from md2py's TreeOfContents.
Here are a few of the most important differences:
>
> - Attribute access is no longer restricted to a node's direct children. It
can include - as BeautifulSoup does - any of the node's descendants.
> - Explicitly access a TOC's `string` attribute to retrieve its contents.

LaTeX2Python offers only one function `tex2py`, which generates a Python
parse tree from Latex. This object is a navigable, "Tree of Contents"
abstraction for the latex file.

Take, for example, the following latex file. ([See pdf](https://github.com/alvinwan/md2py/tests/samples/chikin.pdf))

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
  Chikin Tales   Chikin Scraem
      /            /     \
  Waddling  Plopping    I Scream
```



## Installation

Install via pip.

```
pip install tex2py
```
