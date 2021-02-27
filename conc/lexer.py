from collections import OrderedDict
from concepts import Def, Eval, Int, Obj, Sent, Add

symbolsToClasses = [
    (';', Sent),
    ('DEF', Def),
    ('EVAL', Eval),
    ('+', Add),
    (lambda x: x.isdecimal(), Int),
    (lambda x: True, Obj),
]

def lex(symbols):
    return [find_instance(sym, symbolsToClasses) for sym in symbols]

def find_instance(symbol, symbolsToClasses):
    for symbol_or_pred, cls in symbolsToClasses:
        if symbol_or_pred == symbol:
            return cls()
        elif callable(symbol_or_pred) and symbol_or_pred(symbol):
            return cls(symbol)
