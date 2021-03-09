from concepts import Def, Eval, Int, Obj, Sent, Add, Equals, Ep, Subtract

symbolsToClasses = [
    ('EP', Ep),
    (';', Sent),
    ('::', Def),
    ('$', Eval),
    ('+', Add),
    ('-', Subtract),
    ('=', Equals),
    (lambda x: x.isdecimal(), Int),
    (lambda x: True, Obj),
]

def lex(symbols):
    instances = [find_instance(sym, symbolsToClasses) for sym in symbols]
    for i, ins in enumerate(instances):
        ins.position = i
    return instances

def find_instance(symbol, symbolsToClasses):
    for symbol_or_pred, cls in symbolsToClasses:
        if symbol_or_pred == symbol:
            return cls()
        elif callable(symbol_or_pred) and symbol_or_pred(symbol):
            return cls(symbol)
