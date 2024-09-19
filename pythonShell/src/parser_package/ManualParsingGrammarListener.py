# Generated from src/parser_package/ManualParsingGrammar.g4 by ANTLR 4.13.1
from antlr4 import *

if "." in __name__:
    from .ManualParsingGrammarParser import ManualParsingGrammarParser
else:
    from ManualParsingGrammarParser import ManualParsingGrammarParser


# This class defines a complete listener for a parse tree
# produced by ManualParsingGrammarParser.
class ManualParsingGrammarListener(ParseTreeListener):
    # Enter a parse tree produced by ManualParsingGrammarParser#parse.
    def enterParse(self, ctx: ManualParsingGrammarParser.ParseContext):
        pass

    # Exit a parse tree produced by ManualParsingGrammarParser#parse.
    def exitParse(self, ctx: ManualParsingGrammarParser.ParseContext):
        pass

    # Enter a parse tree produced by ManualParsingGrammarParser#pipeStatement.
    def enterPipeStatement(
        self, ctx: ManualParsingGrammarParser.PipeStatementContext
    ):
        pass

    # Exit a parse tree produced by ManualParsingGrammarParser#pipeStatement.
    def exitPipeStatement(
        self, ctx: ManualParsingGrammarParser.PipeStatementContext
    ):
        pass

    # Enter a parse tree produced by ManualParsingGrammarParser#callStatement.
    def enterCallStatement(
        self, ctx: ManualParsingGrammarParser.CallStatementContext
    ):
        pass

    # Exit a parse tree produced by ManualParsingGrammarParser#callStatement.
    def exitCallStatement(
        self, ctx: ManualParsingGrammarParser.CallStatementContext
    ):
        pass

    # Enter a parse tree produced by ManualParsingGrammarParser#args.
    def enterArgs(self, ctx: ManualParsingGrammarParser.ArgsContext):
        pass

    # Exit a parse tree produced by ManualParsingGrammarParser#args.
    def exitArgs(self, ctx: ManualParsingGrammarParser.ArgsContext):
        pass

    # Enter a parse tree produced by ManualParsingGrammarParser#argsForSub.
    def enterArgsForSub(
        self, ctx: ManualParsingGrammarParser.ArgsForSubContext
    ):
        pass

    # Exit a parse tree produced by ManualParsingGrammarParser#argsForSub.
    def exitArgsForSub(
        self, ctx: ManualParsingGrammarParser.ArgsForSubContext
    ):
        pass

    # Enter a parse tree produced by ManualParsingGrammarParser#substitutionStatement.
    def enterSubstitutionStatement(
        self, ctx: ManualParsingGrammarParser.SubstitutionStatementContext
    ):
        pass

    # Exit a parse tree produced by ManualParsingGrammarParser#substitutionStatement.
    def exitSubstitutionStatement(
        self, ctx: ManualParsingGrammarParser.SubstitutionStatementContext
    ):
        pass

    # Enter a parse tree produced by ManualParsingGrammarParser#statement.
    def enterStatement(self, ctx: ManualParsingGrammarParser.StatementContext):
        pass

    # Exit a parse tree produced by ManualParsingGrammarParser#statement.
    def exitStatement(self, ctx: ManualParsingGrammarParser.StatementContext):
        pass

    # Enter a parse tree produced by ManualParsingGrammarParser#app.
    def enterApp(self, ctx: ManualParsingGrammarParser.AppContext):
        pass

    # Exit a parse tree produced by ManualParsingGrammarParser#app.
    def exitApp(self, ctx: ManualParsingGrammarParser.AppContext):
        pass

    # Enter a parse tree produced by ManualParsingGrammarParser#fileName.
    def enterFileName(self, ctx: ManualParsingGrammarParser.FileNameContext):
        pass

    # Exit a parse tree produced by ManualParsingGrammarParser#fileName.
    def exitFileName(self, ctx: ManualParsingGrammarParser.FileNameContext):
        pass

    # Enter a parse tree produced by ManualParsingGrammarParser#string.
    def enterString(self, ctx: ManualParsingGrammarParser.StringContext):
        pass

    # Exit a parse tree produced by ManualParsingGrammarParser#string.
    def exitString(self, ctx: ManualParsingGrammarParser.StringContext):
        pass


del ManualParsingGrammarParser
