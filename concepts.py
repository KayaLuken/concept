
class ConceptBase:

    def validate_neighbours(self, *args, **kwargs):
        raise NotImplementedError


class A(ConceptBase):
    symbol = 'a'

class All:
    '''
    A x in X
    A of X
    '''

class Assoc:
    '''
    `2 + left assoc 3 * 4 = `assoc 2 + assoc 3 * 4
    equivalent to conventional () usage
    '''

class Bran:
    '''
    Graph construct
    x is bran prop a bran prop b
    '''


class Conc(ConceptBase):
    '''
    Concept
    '''
    sym = 'C'



class Def(ConceptBase):
    '''Definition.'''
    #signature = Re

    symbol = '::'

    def __init__(self, rel):
        self.rel = rel

    @staticmethod
    def _def(rel):
        return rel.signature[0]


class Dist:
    '''
    Macro
    `hold enum dist e1 e2 e3 = `hold e1 enum e2 enum e3
    '''

class Dys:
    '''
    Disjunction
    '''


class Ep:
    '''Epic; series of statements'''
    def __init__(self, concepts):
        pass


class Eq(ConceptBase):
    """Equal to"""

    sym = '='

    def __init__(self, left, right):
        try:
            self.validate_neighbours(left, right)
        except SyntaxError:
            print('Invalid syntax')

    def evaluate(self, left, right):
        return left.value == right.value

    def validate_neighbours(self, left, right):
        pass


class Ex(ConceptBase):
    '''Existential quantifier'''
    symbol = 'E'


class Eval(ConceptBase):
    '''Assertion of factual relationaship'''
    symbol = '$'


class For:
    '''
    nul for ex y
    '''
    def __init__(self, source, target):
        self.source = source
        self.target = target


class Int:
    def __init__(self, v):
        self.v =  v


class Is:pass

class Jun:
    '''Junction. x = 2 Jun 4'''

class Lef:
    def __init__(self, directee):
        '''
        Specifies direction of conceptual graph
        `3 - 2` has an implicit direction of action
        `3 left - 2` semantically equivalent to `2 - 3`
        '''

class Nar:
    '''
    Meta property
    `k nar relation def ..` allows generation of property instances for k instances
    eg k is integer `2 nar relation`
    '''


class Nth:
    '''
    nth 3 of L wich = a b c left wich = 3
    '''

class Nul:
    pass


class Obj:
    def __init__(self, instance):
        '''
        Lowest level concept
        Any undefined symbol is implicitly instantiating object
        `x is y`
        wraps concept and holds in place overriding behaviour
        `obj + is a binary relation`
        '''
        self.instance = instance


class Of:
    '''
    f of x | colour of y
    '''


class Prop:
    '''
    `x is prop x`
    '''


class Quan:
    '''
    pluralises object
    '''

class Re:
    signature = (Obj, Prop)


class Rel:
    'rel as object of its own. not applied'

class Ryt:
    '''
    See left
    '''

class Sent:
    '''Statement. Collects all concepts to the right'''


class Thn:
    '''
    OL = b thn com a com c
    gives order to unordered relation
    fixes it to 2d mapping
    '''


class Stat:
    def __init__(self, *concepts):
        '''
        Outermost concept. Collects all elements to the right
        Opposes definition in that works only with existing truths, not introducing new ones
        Should be able to reach into existing definitions to raise error if given undefined concept
        Invoked implicitly in interpreter unless definition is used
        `This Statement is False` should be valid although statement is an inner concept
        In this case Statement must have different behaviour, changed by `This` selector
        This modification and changing precedence is a common pattern but this case is more circular
        eg `This Integer is Even` doesnt achieve the same circularity
        meaning of `this` collapses into `that`, as in `that statement is false` and is ambiguous
        `previous` and `next` are unambiguous selectors, eg
        `next statement is false | previous statement is true`
        note: could add `the` quantifier, but this is redundant in this case
        '''

class Sym:
    '''
    Points to symbol itself and not the concept it represents
    `symbol x ~ `
    Could be used in building macros
    '''

class Vers:
    pass


class Wer:
    '''
    Allows inline definition
    x = y wer x con y is int
    '''


class Wich:
    '''
    An aside, makes previous conc the subject
    `x wich is a Int /wich = 3`
    Awkward syntax squashing graph contruct into 1D structure
    alternative `x wich3 is a int = 3`
    '''


class Zi(Re):
    signature = Re.signature