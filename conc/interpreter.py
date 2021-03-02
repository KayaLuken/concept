from conc.lexer import lex
from conc.parser_ import parse
from conc.store import Store


class Interpreter():

    def __init__(self):
        self.store = Store()

    def interpret(self, s: str):
        parsed = parse(s)
        lexed = lex(parsed)
        un_assembled = self.assemble(lexed)
        if any(un_assembled):
            raise SyntaxError("Unassembled concepts remaining")
        self.output = self.run()
        if len(self.output) == 1:
            self.output = self.output[0]

    def assemble(self, lexed):
        self.ep = lexed[0]
        return self.ep.assemble(lexed)

    def run(self):
        return self.ep.run()
