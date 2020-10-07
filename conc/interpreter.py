from conc.lexer import lex
from conc.parser_ import parse
from conc.store import Store


class Interpreter():

    def __init__(self):
        self.store = Store()

    def interpret(self, s: str):
        parsed = parse(s)
        lexed = lex(parsed)
        self.assemble(lexed)
        self.output = self.run()

    def assemble(self, lexed):
        self.sent = lexed[-1]
        return self.sent.assemble(lexed[:-1])

    def run(self):
        return self.sent.eval()
