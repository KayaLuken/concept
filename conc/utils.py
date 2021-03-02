from more_itertools import locate


def find(pred, xs):
    try:
        index = list(locate(xs, pred))[0]
        return index, xs[index]
    except IndexError:
        return None, None