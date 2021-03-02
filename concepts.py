from more_itertools import locate

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
        concept = self.get_next_concept(self.position, lexed)

        self.child = concept

        if concept.is_terminal:
            lexed[concept.position] = None
            return lexed
        else:
            return concept.assemble(lexed)

    def get_next_concept(self, lexed, position):
        raise NotImplemented

    def run(self):
        return self.child.run()


class BinaryConcept(ConceptBase):
    def assemble(self, lexed):
        lexed[self.position] = None
        concepts, next_positions = self.get_next_concepts(self.position, lexed)

        self.children = concepts

        if not self.validate(concepts):
            raise SyntaxError

        if concepts[0].is_terminal and concepts[1].is_terminal:
            lexed[next_positions[0]] = None
            lexed[next_positions[1]] = None
            return lexed

    def get_next_concepts(self, position, lexed):
        raise NotImplemented

class InfinaryConcept(ConceptBase):
    def assemble(self, lexed):
        lexed[self.position] = None
        concepts = self.get_next_concepts(self.position, lexed)
        self.children = concepts

        for conc in concepts:
            lexed = conc.assemble(lexed)

        return lexed

    def get_next_concepts(self, position, lexed):
        raise NotImplemented

    def run(self):
        return [child.run() for child in self.children]

class Int(TerminalConcept):
    def __init__(self, value):
        self.value = int(value)


class Add(BinaryConcept):

    def validate(self, concepts):
        return type(concepts[0]) is Int and type(concepts[1]) is Int

    def get_next_concepts(self, position, lexed):
        return [lexed[position - 1], lexed[position + 1]], [position - 1, position + 1]

    def run(self):
        return self.children[0].run() + self.children[1].run()


class Equals(BinaryConcept):

    def validate(self, concepts):
        return type(concepts[0]) is Int and type(concepts[1]) is Int

    def get_next_concepts(self, position, lexed):
        return [lexed[position - 1], lexed[position + 1]], [position - 1, position + 1]

    def run(self):
        return self.children[0].run() == self.children[1].run()


class Def(ConceptBase):
    symbol = '::'


class Eval(UnaryConcept):

    def get_next_concept(self, position, lexed):
        next_none_indices = list(locate(lexed[position:], lambda c: c is None))
        other_none_indices = len(next_none_indices) > 1
        if other_none_indices:
            next_none_index = next_none_indices[1]
            next_none_index += position
            return find_highest_precedence_concept(lexed[position:next_none_index])
        else:
            return find_highest_precedence_concept(lexed[position:])



class Obj(TerminalConcept):
    pass


class Sent(UnaryConcept):
    '''Statement. Collects all concepts to the left'''

    def get_next_concept(self, position, lexed):
        first_unconsumed_concept = find(lambda c: c is not None, lexed)
        if type(first_unconsumed_concept) not in {Eval, Def}:
            raise SyntaxError("Sentence must be evaluation or definition")
        return lexed[first_unconsumed_concept.position]

class Ep(InfinaryConcept):

    def get_next_concepts(self, position, lexed):
        instances = get_concept_instances(Sent, lexed)
        if not instances or not isinstance(lexed[-1], Sent):
            raise SyntaxError("Improper placement of sentences")
        return instances
