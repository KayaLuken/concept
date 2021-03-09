from more_itertools import locate, split_at

from conc.utils import find


def find_highest_precedence_concept(concepts):
    remaining_concepts = filter(lambda x: x, concepts)
    precedences = [c.precedence for c in remaining_concepts]
    min_precedence = min(precedences)
    has_min_precedence = lambda c: c and c.precedence == min_precedence
    return find(has_min_precedence, concepts)




def get_concept_instances(concept, concepts):
    return list(filter(lambda c: type(c) is concept, concepts))


class ConceptBase:
    is_terminal = False
    position = None

    @property
    def precedence(self):
        from conc.lexer import symbolsToClasses
        return list(locate(symbolsToClasses, lambda x: x[1] is type(self)))[0]


class TerminalConcept(ConceptBase):
    is_terminal = True

    def __init__(self, value):
        self.value = value

    def run(self):
        return self.value


class UnaryConcept(ConceptBase):
    def assemble(self, lexed):
        lexed[self.position] = None
        concept = self.get_next_concept(lexed)

        self.child = concept

        if concept.is_terminal:
            lexed[concept.position] = None
            return lexed
        else:
            return concept.assemble(lexed)

    def get_next_concept(self, lexed):
        raise NotImplemented

    def run(self):
        return self.child.run()


class BinaryConcept(ConceptBase):
    def assemble(self, lexed):
        lexed[self.position] = None
        concepts = self.get_next_concepts(lexed)

        self.children = concepts

        if not self.validate(concepts):
            raise SyntaxError

        if concepts[0].is_terminal and concepts[1].is_terminal:
            lexed[concepts[0].position] = None
            lexed[concepts[1].position] = None
            return lexed

    def get_next_concepts(self, lexed):
        return [lexed[self.position - 1], lexed[self.position + 1]]

class InfinaryConcept(ConceptBase):
    def assemble(self, lexed):
        lexed[self.position] = None
        concepts = self.get_next_concepts(lexed)
        self.children = concepts

        for conc in concepts:
            lexed = conc.assemble(lexed)

        return lexed

    def get_next_concepts(self, lexed):
        raise NotImplemented

    def run(self):
        return [child.run() for child in self.children]

class Int(TerminalConcept):
    def __init__(self, value):
        self.value = int(value)


class ArithmeticConcept(BinaryConcept):

    def is_arithmetic_concept(self, concept):
        return issubclass(type(concept), ArithmeticConcept) or issubclass(type(concept), TerminalConcept)

    def validate(self, concepts):
        return self.is_arithmetic_concept(concepts[0]) and self.is_arithmetic_concept(concepts[1])


class Add(ArithmeticConcept):
    def run(self):
        return self.children[0].run() + self.children[1].run()


class Subtract(ArithmeticConcept):
    def run(self):
        return self.children[0].run() - self.children[1].run()


class Equals(BinaryConcept):

    def validate(self, concepts):
        are_ints = type(concepts[0]) is Int and type(concepts[1]) is Int
        are_objects = type(concepts[0]) is Obj and type(concepts[1]) is Obj
        return are_ints or are_objects

    def run(self):
        return self.children[0].run() == self.children[1].run()


class Def(ConceptBase):
    symbol = '::'


class Eval(UnaryConcept):

    def get_next_concept(self, lexed):
        current_block = list(split_at(lexed[self.position+1:], lambda c: c is None))[0]
        return find_highest_precedence_concept(current_block)


class Obj(TerminalConcept):
    pass


class Sent(UnaryConcept):
    '''Statement. Collects all concepts to the left'''

    def get_next_concept(self, lexed):
        first_unconsumed_concept = find(lambda c: c is not None, lexed)
        if type(first_unconsumed_concept) not in {Eval, Def}:
            raise SyntaxError("Sentence must be evaluation or definition")
        return lexed[first_unconsumed_concept.position]

class Ep(InfinaryConcept):

    def get_next_concepts(self, lexed):
        instances = get_concept_instances(Sent, lexed)
        if not instances or not isinstance(lexed[-1], Sent):
            raise SyntaxError("Improper placement of sentences")
        return instances
