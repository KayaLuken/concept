import inspect as ins


class ConceptBase:
    white_list = []

    @property
    def is_terminal(self):
        return len(self.white_list) == 0

    def is_valid(self, sym):
        literal_match = sym.__class__ in self.white_list
        predicate_match = any(ins.isfunction(pred) and pred(sym) for pred in self.white_list)
        return literal_match or predicate_match


class Def(ConceptBase):
    symbol = '::'


class Eval(ConceptBase):
    '''Assertion of factual relationship'''
    symbol = '$'

    white_list = [lambda x: hasattr(x, 'eval')]

    def assemble(self, lexed):
        sym = lexed[0]
        if not self.is_valid(sym):
            raise SyntaxError

        self.children = sym

        if sym.is_terminal:
            return lexed
        else:
            return sym.assemble(lexed[1:])

    def eval(self):
        return self.children.eval()


class Int(ConceptBase):

    def __init__(self, value):
        self.value = value


    def eval(self):
        return self.value

class Obj(ConceptBase):
    pass


class Sent(ConceptBase):
    '''Statement. Collects all concepts to the left'''
    white_list = [Def, Eval]

    def assemble(self, lexed):
        sym = lexed[0]
        if not self.is_valid(sym):
            raise SyntaxError

        self.children = sym

        if sym.is_terminal:
            return lexed
        else:
            return sym.assemble(lexed[1:])

    def eval(self):
        return self.children.eval()
