from inspect import isfunction
from more_itertools import locate

from conc.utils import find


def find_highest_precedence_concept(concepts):
    remaining_concepts = filter(lambda x: x, concepts)
    precedences = [c.precedence for c in remaining_concepts]
    min_precedence = min(precedences)
    has_min_precedence = lambda c: c and c.precedence == min_precedence
    index = list(locate(concepts, has_min_precedence))[0]
    return concepts[index], index


class ConceptBase:
    is_terminal = False

    @property
    def precedence(self):
        from conc.lexer import symbolsToClasses
        return list(locate(symbolsToClasses, lambda x: x[1] is type(self)))[0]

    def get_next_concepts(self, lexed, position):
        raise NotImplemented

    def validate(self, concept):
        raise NotImplemented


class TerminalConcept(ConceptBase):
    is_terminal = True

    def __init__(self, value):
        self.value = value

    def run(self):
        return self.value


class UnaryConcept(ConceptBase):
    def assemble(self, lexed, position):
        lexed[position] = None
        concept, next_position = self.get_next_concepts(lexed, position)

        self.child = concept

        if not self.validate(concept):
            raise SyntaxError

        if concept.is_terminal:
            lexed[next_position] = None
            return lexed
        else:
            return concept.assemble(lexed, next_position)

    def run(self):
        return self.child.run()


class BinaryConcept(ConceptBase):
    def assemble(self, lexed, position):
        lexed[position] = None
        concepts, next_positions = self.get_next_concepts(lexed, position)

        self.children = concepts

        if not self.validate(concepts):
            raise SyntaxError

        if concepts[0].is_terminal and concepts[1].is_terminal:
            lexed[next_positions[0]] = None
            lexed[next_positions[1]] = None
            return lexed


class Int(TerminalConcept):
    def __init__(self, value):
        self.value = int(value)


class Add(BinaryConcept):

    def validate(self, concepts):
        return type(concepts[0]) is Int and type(concepts[1]) is Int

    def get_next_concepts(self, lexed, position):
        return [lexed[position - 1], lexed[position + 1]], [position - 1, position + 1]

    def run(self):
        return self.children[0].run() + self.children[0].run()


class Equals(BinaryConcept):

    def validate(self, concepts):
        return type(concepts[0]) is Int and type(concepts[1]) is Int

    def get_next_concepts(self, lexed, position):
        return [lexed[position - 1], lexed[position + 1]], [position - 1, position + 1]

    def run(self):
        return self.children[0].run() == self.children[0].run()


class Def(ConceptBase):
    symbol = '::'


class Eval(UnaryConcept):

    def validate(self, concept):
        return True

    def get_next_concepts(self, lexed, position):
        return find_highest_precedence_concept(lexed)


class Obj(TerminalConcept):
    pass


class Sent(UnaryConcept):
    '''Statement. Collects all concepts to the left'''

    def validate(self, concept):
        return type(concept) is Def or type(concept) is Eval

    def get_next_concepts(self, lexed, position):
        return lexed[0], 0
