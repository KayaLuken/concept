from conc.assembler import assemble
from conc.graph import Graph
from conc.lexer import lex
from conc.parser_ import parse
from conc.runner import run



class Interpreter():

    def __init__(self):
        self.graph = Graph()

    def interpret(self, s: str):
        parsed = parse(s)
        lexed = lex(parsed)
        assembled = assemble(lexed)
        self.output = run(assembled, self.graph)

