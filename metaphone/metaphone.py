# -*- coding: utf-8 -*-

# EDIT configs/default.ini TO CHANGE SETTINGS
from config import config

from .singlemetaphone import *
from .doublemetaphone import *


class UnknownMetaphoneAlg(Exception):
    pass


def metaphone(s, alg = None):
    if alg == None:
        alg = config.use_metaphone_alg

    if alg == "single":
        return singlemetaphone(s)
    elif alg == "double":
        pair = doublemetaphone(s)
        if pair[0] == pair[1]:
            return pair[0]
        else:
            return pair
    elif alg == "double[0]":
        pair = doublemetaphone(s)
        return pair[0]
    elif alg == "double[1]":
        pair = doublemetaphone(s)
        return pair[1]

    # If we don't recognize metaphone algorithm, throw an exception.
    raise UnknownMetaphoneAlg("Did not recognize metaphone algorithm '%s'" % config.use_metaphone_alg)


def compare_metaphone(m1, m2):
    # Return whether some part of single or double metaphone match
    # We assume that m1 and m2 are either strings or tuple of two strings
    is_string_1 = isinstance(m1, basestring)
    is_string_2 = isinstance(m2, basestring)

    if is_string_1 and is_string_2:
        return m1 == m2
    elif is_string_1 and not is_string_2:
        return m1 == m2[0] or m1 == m2[1]
    elif not is_string_1 and is_string_2:
        return m1[0] == m2 or m1[1] == m2
    else: # Both are tuples
        return m1[0] == m2[0] or m1[0] == m2[1] or m1[1] == m2[0] or m1[1] == m2[1]
