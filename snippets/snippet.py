__author__ = 'cole'

median_lambda = lambda l: l[len(l) // 2] if (len(l) & 1) else sum(l[(len(l) // 2 - 1):][:2]) / 2.0


def median_value_in_list(l):
    # a slightly more legible version of `median_lambda`
    mid = len(l) // 2
    return l[mid] if len(l) & 1 else sum(l[mid - 1:][:2]) / 2.0