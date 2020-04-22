from collections import OrderedDict
from typing import List, Type

from concepts import ConceptBase, Def, Eval, Int, Obj, Is, Sent

symbolsToClasses = {
    'DEF': Def,
    'IS': Is,
    'EVAL': Eval,
    ';': Sent,
}


def lex(symbols: List[str]) -> List[Type[ConceptBase]]:
    return [symbolsToClasses.get(sym) or get_or_create_instance(sym) for sym in symbols]


def get_or_create_instance(sym: symbolsToClasses.keys()):
    predicatesToInstances = OrderedDict([
        (lambda x: x.isdecimal(), lambda x: Int(x)),
        (lambda x: True, lambda x: Obj(x)),
    ])
    for p in predicatesToInstances:
        if p(sym):
            # todo check graph for presence of object instance
            return predicatesToInstances[p](sym)

