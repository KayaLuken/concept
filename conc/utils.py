from more_itertools import locate


def find(pred, xs):
    return list(filter(pred, xs))[0]