# Generated from D:/Programming/comp0010-shell-python-p28/src/parser_package/ManualParsingGrammar.g4 by ANTLR 4.13.1
from antlr4 import *

if "." in __name__:
    from .ManualParsingGrammarParser import ManualParsingGrammarParser
else:
    from ManualParsingGrammarParser import ManualParsingGrammarParser


class ManualParsingGrammarVisitor(ParseTreeVisitor):
    """
     This class defines a complete generic visitor for a parse tree produced by ManualParsingGrammarParser. The visitor uses a combination
     of ANTLR context parsing and a command_stack implementation to return a list of strings representing command execution sequence.
     """

    def __init__(self):
        """
           Initialize the ManualParsingGrammarVisitor.

           Attributes:
           - command_stack (list): A stack to keep track of parsed commands.
           """
        self.command_stack = []

    # Visit a parse tree produced by ManualParsingGrammarParser#pipeStatement.
    def visitPipeStatement(
        self, ctx: ManualParsingGrammarParser.PipeStatementContext
    ):
        """
               Visit a parse tree produced by ManualParsingGrammarParser#pipeStatement.

               Constructs pipe statements and nested pipe statements (for multiple pipe statements)
                by popping elements from the command stack, and appends result to
                the command_stack

               Args:
               - ctx (ManualParsingGrammarParser.PipeStatementContext): The parse tree context.

               Returns:
               None
               """
        for child_ctx in ctx.getChildren():
            if not child_ctx.getText() == "|":
                self.visit(child_ctx)

        self.command_stack.reverse()

        lhs = self.command_stack.pop()
        rhs = self.command_stack.pop()
        pipe = ["Pipe", lhs, rhs]
        while self.command_stack:
            lhs = self.command_stack.pop()
            pipe = ["Pipe", pipe, lhs]

        self.command_stack.append(pipe)

    # Visit a parse tree produced by ManualParsingGrammarParser#callStatement.
    def visitCallStatement(
        self, ctx: ManualParsingGrammarParser.CallStatementContext
    ):
        """
               Visit a parse tree produced by ManualParsingGrammarParser#callStatement.

               Extracts apps (echo, grep ...) and arguments and formats information
               into a call statement list, and appends result to the command_stack

               Args:
               - ctx (ManualParsingGrammarParser.CallStatementContext): The parse tree context.

               Returns:
               None
               """
        app = ctx.app().getText()
        args = [
            ctx.args().getText().strip() if ctx.args() != None else ""
        ].pop()
        if "'" in args:
            args = args.replace("'", "")
        if '"' in args:
            args = args.replace('"', "")
        self.command_stack.append(["Call", app, args])

    def visitCallStatementOnDemand(self, cmd):
        """
               Visit a call statement and extract details from a command to return
               a call statement list on demand

               Args:
               - cmd (str): Call statement content (not the context)

               Returns:
               list: A formatted call command.
               """
        app = cmd.split()[0]
        args = " ".join(cmd.split()[1:])
        if "'" in args:
            args = args.replace("'", "")
        if '"' in args:
            args = args.replace('"', "")
        call = ["Call", app, args]
        return call

    # Visit a parse tree produced by ManualParsingGrammarParser#substitutionStatement.
    def visitSubstitutionStatement(
        self, ctx: ManualParsingGrammarParser.SubstitutionStatementContext
    ):
        """
                Visit a parse tree produced by ManualParsingGrammarParser#substitutionStatement.

                Extract and format information from a substitution statement, and appends result to
                the command_stack

                Args:
                - ctx (ManualParsingGrammarParser.SubstitutionStatementContext): The parse tree context.

                Returns:
                None
                """
        self.visit(ctx.statement())
        command = self.visitCallStatementOnDemand(ctx.app().getText())
        toNest = self.command_stack.pop()
        if ctx.args() and ctx.args().getText().strip() != '"':
            toNest[-1] = ctx.args().getText().strip() + toNest[-1]
        if ctx.argsForSub() and ctx.argsForSub().getText().strip() != '"':
            toNest[-1] = toNest[-1] + ctx.argsForSub().getText().strip()
        command[-1] = toNest
        self.command_stack.append(command)

    def get_command_details(self):
        """
              Get details of the parsed command.

              Returns:
              list: Details of the parsed command.
              """
        if self.command_stack:
            return self.command_stack[0]


del ManualParsingGrammarParser