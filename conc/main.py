
from conc.assembler import assemble
from conc.graph import Graph
from conc.lexer import lex
from conc.parser_ import parse
from conc.runner import run

graph = Graph()

def interpret(s: str):
    parsed = parse(s)
    lexed = lex(parsed)
    assembled = assemble(lexed)
    return run(assembled, graph)

