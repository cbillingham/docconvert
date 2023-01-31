"""Base python module parser class."""

import ast
import sys
import tokenize
from collections import namedtuple


Token = namedtuple("Token", ["kind", "value", "start", "end", "source"])
"""Token class for wrapping python token data.

Note:
    Python 3 tokenize already returns namedtuples, but because python 2
    only return tuples, we wrap them all into this custom class.

Attributes:
    kind (int): The python token kind (see :py:mod:`tokenize` for
        token definitions). (e.g. tokenize.TILDE)
    value (str): The token value. (e.g. "~")
    start (tuple(int, int)): A 2-tuple ``(srow, scol)`` of ints
        specifying the row and column where the token begins in the
        source.
    end (tuple(int, int)): A 2-tuple ``(erow, ecol)`` of ints
        specifying the row and column where the token ends in the
        source.
    source (int): The entire line on which the token was found.
"""


RawDocstring = namedtuple(
    "RawDocstring", ["start", "end", "lines", "args", "keywords", "vararg", "kwarg"]
)
"""RawDocstring class for storing raw docstring information.

Attributes:
    start (int): The starting line number of the docstring in the
        module file.
    end (int): The ending line number of the docstring in the
        module file
    lines (list(str)): The text contents of the docstring.
    args (list(str)): A list of arguments for a function docstring.
    keywords (list(str)): A list of keyword arguments for a function
        docstring.
    vararg (str or None): The name of the variable argument to a
        function docstring.
    kwarg (str or None): The name of the variable keyword argument to a
        function docstring.
"""


def default_docstring(start, end, lines):
    """Convenience function for creating default docstring without args.

    Args:
        start (int): The starting line number of the docstring in the
            module file.
        end (int): The ending line number of the docstring in the
            module file
        lines (list(str)): The text contents of the docstring.

    Returns:
        RawDocstring: A docstring that is initialized as follows::

            RawDocstring(
                start=start,
                end=end,
                lines=lines,
                args=[],
                keywords=[],
                vararg=None,
                kwarg=None,
            )
    """
    return RawDocstring(start, end, lines, [], [], None, None)


class TokenStream(object):
    """Wrapper iterator around tokenize generator to manage token stream."""

    def __init__(self, generator):
        """
        Args:
            generator (generator): A token generator that generates
                5-tuples that include (token kind, value,
                start line number, end line number, original source).
        """
        self._generator = generator
        current = next(self._generator, None)
        self.current = Token(*current) if current else None

    def __next__(self):
        """Gets the next tokens and increments the current token.

        Returns:
            Token: The current token.

        Raises:
            StopIteration: If the iterator is exhausted.
        """
        return self.next()

    def __iter__(self):
        """Returns iterator object for iterating over the tokens.

        Returns:
            LineIter: The iterator over the lines.
        """
        return self

    def next(self):
        """Gets the next tokens and increments the current token.

        Returns:
            Token: The current token.

        Raises:
            StopIteration: If the iterator is exhausted.
        """
        if not self.current:
            raise StopIteration
        current = self.current
        new_token = next(self._generator, None)
        self.current = Token(*new_token) if new_token else None
        return current

    def skip(self, kinds=(), values=()):
        """Skip through tokens of the specified kinds or values.

        Args:
            kinds (Iterable(int)): List of token kinds to skip.
            values (Iterable(int)): List of token values to skip.
        """
        while self.current and (
            self.current.kind in kinds or self.current.value in values
        ):
            self.next()

    def skip_until(self, kinds=(), values=()):
        """Skip through tokens until a matching token is found.

        Tokens will be skipped until one is found that matches one of
        the specified kinds or values.

        Args:
            kinds (Iterable(int)): List of token kinds to skip until.
            values (Iterable(int)): List of token values to skip until.
        """
        while self.current:
            if self.current.kind in kinds or self.current.value in values:
                break
            self.next()

    def consume(self, kind):
        """Consume current token and check kind.

        Args:
            kind (int): Expected token kind of the current token.
        """
        if self.current:
            assert self.current.kind == kind
            self.next()


class ModuleParser(object):
    """Class for parsing through lines of file to find all docstrings.

    Attributes:
        docstrings (list(RawDocstring)): The list of docstrings found in
            this python module after running :py:meth:`parse()`.
    """

    def __init__(self, lines):
        """
        Args:
            lines (list(str)): The source lines of the file.
        """
        self.lines = lines
        self.current_line_num = 0
        self.docstrings = []
        self._siblings = []

    def _get_next_line(self):
        """Callable for getting lines.

        Returns the current line and increments current line. Returns
        an empty string to denote the end of the lines.

        Note:
            For use with ``_get_tokens()`` because tokenize
            expects a callable function that returns lines.

        Returns:
            str: The current line.
        """
        line = ""
        if self.current_line_num < len(self.lines):
            line = self.lines[self.current_line_num]
            self.current_line_num += 1
        return line

    def _get_tokens(self, start):
        """Gets token stream for tokens starting at a specific line.

        Args:
            start (int): The line to start at.

        Returns:
            TokenStream: A stream of Token namedtuples.
        """
        # take advantage of tokenize.generate_tokens:
        #     an undocumented, backwards compatible, API for using
        #     tokenize with strings
        self.current_line_num = start
        generator = tokenize.generate_tokens(self._get_next_line)
        return TokenStream(generator)

    def _find_docstring(self, tokens, start):
        """Find exact line start and line end of the docstring.

        Args:
            tokens (TokenStream): A token stream object.
            start (int): The starting line of the definition.

        Returns:
            tuple(int, int) or None: Tuple containing start and end line
            of docstring if it exists, else None.
        """
        # calculate line index offset because token lines start at 1
        # and are relative to the starting line
        docstring = None
        line_offset = start - 1
        tokens.skip(kinds=(tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE))
        if tokens.current and tokens.current.kind == tokenize.STRING:
            docstring = (
                tokens.current.start[0] + line_offset,
                tokens.current.end[0] + line_offset + 1,
            )
        return docstring

    def _parse_definition(self, start):
        """Parse through start of class or func def and find docstring.

        Args:
            start (int): The starting line of the definition.

        Returns:
            tuple(int, int) or None: Tuple containing start and end line
            of docstring if it exists, else None.
        """
        docstring = None
        tokens = self._get_tokens(start)
        # skip decorators
        tokens.skip_until(values=("def", "class"))
        while tokens.current:
            if tokens.current.kind == tokenize.NEWLINE:
                tokens.consume(tokenize.NEWLINE)
                tokens.skip(kinds=(tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE))
                # if there is no indent after the definition then we
                # skip because one line functions cannot have docstrings
                if tokens.current and tokens.current.kind == tokenize.INDENT:
                    tokens.consume(tokenize.INDENT)
                    docstring = self._find_docstring(tokens, start)
                break
            # skip through multi-line args, kwargs, and annotations
            tokens.next()
        return docstring

    def _visit_module(self, node):
        """Add module docstring if it exists.

        Args:
            node (ast.Module): The ast node defining a Python module.
        """
        first_line = 0
        tokens = self._get_tokens(first_line)
        docstring = self._find_docstring(tokens, first_line)
        if docstring:
            start, end = docstring
            self.docstrings.append(default_docstring(start, end, self.lines[start:end]))

        children = ast.iter_child_nodes(node)
        self._siblings.append(children)
        for child in children:
            self._generic_visit(child)
        self._siblings.pop()

    def _visit_functiondef(self, node):
        """Add function docstring if it exists.

        Args:
            node (ast.FunctionDef): The ast node defining the start of
                a function definition.
        """
        docstring = self._parse_definition(node.lineno - 1)
        if docstring:
            start, end = docstring
            all_args = _get_arguments(node.args)
            self.docstrings.append(
                RawDocstring(start, end, self.lines[start:end], *all_args)
            )

        children = ast.iter_child_nodes(node)
        self._siblings.append(children)
        for child in children:
            self._generic_visit(child)
        self._siblings.pop()

    def _visit_asyncfunctiondef(self, node):
        """Add function docstring if it exists.

        Args:
            node (ast.AsyncFunctionDef): The ast node defining the start of
                a function definition.
        """
        return self._visit_functiondef(node)

    def _visit_classdef(self, node):
        """Add class docstring if it exists.

        Args:
            node (ast.ClassDef): The ast node defining the start of
                a class definition.
        """
        docstring = self._parse_definition(node.lineno - 1)
        if docstring:
            start, end = docstring
            self.docstrings.append(default_docstring(start, end, self.lines[start:end]))

        children = ast.iter_child_nodes(node)
        self._siblings.append(children)
        for child in children:
            self._generic_visit(child)
        self._siblings.pop()

    def _visit_assign(self, node):
        """Add an attribute docstring, if the node is an attribute assignment.

        Args:
            node (ast.Assign): The ast node defining an assignment.
        """
        siblings = self._siblings[-1]
        next_sibling = next(siblings, None)
        if isinstance(next_sibling, ast.Expr) and _is_string_node(next_sibling.value):
            start, end = _get_string_start_end(next_sibling.value)
            self.docstrings.append(default_docstring(start, end, self.lines[start:end]))

    def _generic_visit(self, node):
        """Visit a node.

        Either the visit method specific to the type of node is called,
        or the children of the node are visited.

        Args:
            node (ast.Node): An AST node, of any type, to visit.
        """
        node_type = node.__class__.__name__.lower()
        visit_func = getattr(self, "_visit_" + node_type, None)
        if visit_func:
            visit_func(node)
        # Skip anything that creates a new scope because we only want
        # to visit Assign nodes that are in modules or classes.
        elif node_type not in ("lambda", "genexpr"):
            children = ast.iter_child_nodes(node)
            self._siblings.append(children)
            for child in children:
                self._generic_visit(child)
            self._siblings.pop()

    def parse(self):
        """Parse python file for docstrings.

        Walk abstract syntax tree of file and parse module, function,
        and class docstrings. Each docstring found will be appended to
        the docstrings attribute.
        """
        self.current_line_num = 0
        self.docstrings = []
        self._siblings = []
        source = "".join(self.lines)
        tree = ast.parse(source)
        self._generic_visit(tree)


def _get_arguments(arguments):
    """Get arguments and keywords from arguments.

    Args:
        arguments (ast.arguments): An ast arguments object.

    Returns:
        tuple(list(str), list(str)): A 2-tuple containing list of arg
        names and list of keyword names.
    """
    args = []
    keywords = []
    vararg = None
    kwarg = None
    num_args = len(arguments.args) - len(arguments.defaults)

    for arg in arguments.args[:num_args]:
        args.append(_get_arg_name(arg))
    if arguments.vararg:
        vararg = _get_var_arg(arguments.vararg)

    for keyword in arguments.args[num_args:]:
        keywords.append(_get_arg_name(keyword))
    if sys.version_info[0] >= 3:
        for keyword in arguments.kwonlyargs:
            keywords.append(_get_arg_name(keyword))
    if arguments.kwarg:
        kwarg = _get_var_arg(arguments.kwarg)
    return args, keywords, vararg, kwarg


def _get_var_arg(arg):
    """Helper function to get var arg name depending on py version."""
    # before version 3.4 varargs were saved in the ast as str
    if sys.version_info < (3, 4):
        return arg
    return arg.arg


def _get_arg_name(arg):
    """Helper function to get arg name for any py version."""
    # in python 2 args are stored as Name objects in the ast
    if sys.version_info[0] < 3:
        return arg.id
    return arg.arg


def _is_string_node(node):
    """Check if ast node is a string constant for any py version."""
    # before version 3.8 strings were ast.Str
    if sys.version_info < (3, 8):
        return isinstance(node, ast.Str)
    # after version 3.8 strings are ast.Constant
    else:
        return isinstance(node, ast.Constant) and isinstance(node.s, str)


def _get_string_start_end(node):
    """Get the start and end line for a string ast node."""
    # before version 3.8 node.lineno was end
    if sys.version_info < (3, 8):
        start = node.lineno - node.s.count("\n") - 1
        end = node.lineno
    # after version 3.8 node.lineno is start and node.lineno_end is end
    else:
        start = node.lineno - 1
        end = node.end_lineno
    return start, end
