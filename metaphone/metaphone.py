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
        return pair[0]

    # If we don't recognize metaphone algorithm, throw an exception.
    raise UnknownMetaphoneAlg("Did not recognize metaphone algoritm '%s'" % config.use_metaphone_alg)
