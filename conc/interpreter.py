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

    def assemble(self, lexed):
        # just get the last concept for now, until we have multiple sentences
        self.sent = lexed[-1]
        lexed[-1] = None
        return self.sent.assemble(lexed, -1)

    def run(self):
        return self.sent.run()
