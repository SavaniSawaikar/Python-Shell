'''
The main shell receives command input.
If sequencing (;) is present, the command is split into individual sequence
sections and each of them is processed individually.

First, the command is passed through a visitor
based on ANTLR grammar which will parse the statement
and return a list of strings:

    1. For Call statements:

    Simple statements involving an application
    (echo, grep, cut ...)and some arguments are parsed and
    returned in the form ["Call", app, args]

    2. For Pipe statements:

        2.1. For simple pipe statements (of form a | b),
        the left hand side and right hand side
        statements are parsed, and returned in the form
        ["Pipe", ["Call", app, args], ["Call", app, args]]

        2.2. For multiple pipes (of form a|b|c and so on),
        the left hand side statement will be considered
        a pipe itself and the overall return will be of the form
        ["Pipe",  ["Pipe", ["Call", app, args], ["Call", app, args]], ["Call", app, args]]  # noqa: E501

    3. For command substitution statements:

        Substitutions are considered as statements nested
        inside an overall Call statement.
        Depending on whether the
        statement enclosed in backticks (`) is a Call or Pipe statement,
        it will be nested inside an overall Call statement.
        For instance, "echo `echo a`" would be represented in the form
        ["Call" , "echo" , ["Call", "echo", "a"]].

        If there are any arguments to the left or right of the substitution,
        that is also taken into account in the list returned.
        For instance, "echo a`echo b`c" would be represented in the form
        ["Call" , "echo" , ["Call", "echo", "abc"]].


After the visitor returns the appropriate list,
it is passed to the Converter class, which will convert the list of
strings into a Call object(for inputs of type ["Call", app, args])
or Pipe object(for inputs of type ["Pipe", app, args]).

Then, this object is passed to the Evaluator class
which will call the appropriate eval function based on whether
the input is a Call or Pipe object,
and the eval functions will carry out their process, writing to out.

Finally, the main function prints out the results in out,
and the program terminates.
'''

import re
import sys
import os
from collections import deque
from antlr4 import InputStream, CommonTokenStream
from parser_package import ManualParsingGrammarLexer
from parser_package import ManualParsingGrammarParser
from parser_package import Evaluator
from parser_package import Converter
from parser_package import ManualParsingGrammarVisitor


def eval(cmd, out):
    input_stream = str(InputStream(cmd))
    input_stream = (
        input_stream.split(";")
        if "';'" not in input_stream
        else [input_stream]
    )
    for i in range(len(input_stream)):
        input_stream[i] = input_stream[i].strip()
        input = InputStream(input_stream[i])

        lexer = ManualParsingGrammarLexer(input)
        token_stream = CommonTokenStream(lexer)
        parser = ManualParsingGrammarParser(token_stream)

        parse_tree = parser.parse()

        visitor = ManualParsingGrammarVisitor()
        converter = Converter()
        evaluator = Evaluator()

        visitor.visit(parse_tree)
        command_stack = visitor.get_command_details()
        converted_object = converter.convert_to_objects(command_stack)
        evaluator.evaluate(converted_object, out)


if __name__ == "__main__":
    args_num = len(sys.argv) - 1
    if args_num > 0:
        if args_num != 2:
            raise ValueError("wrong number of command line arguments")
        if sys.argv[1] != "-c":
            raise ValueError(f"unexpected command line argument {sys.argv[1]}")
        out = deque()
        cmdline = re.sub(r"\s*([`|])\s*", r"\1", sys.argv[2])
        eval(cmdline, out)
        while len(out) > 0:
            print(out.popleft(), end="")
    else:
        while True:
            print(os.getcwd() + "> ", end="")
            cmdline = input()
            out = deque()
            eval(cmdline, out)
            while len(out) > 0:
                print(out.popleft(), end="")
