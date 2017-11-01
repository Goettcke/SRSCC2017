# -*- coding: utf-8 -*-

# EDIT configs/default.ini TO CHANGE SETTINGS
from config import config

from .singlemetaphone import *
from .doublemetaphone import *


class UnknownMetaphoneAlg(Exception):
    pass


def metaphone(s):
    # A helper that uses the config to determine what metaphone algorithm to use.

    if not config.use_metaphone:
        return s

    if config.use_metaphone_alg == "single":
        return singlemetaphone(s)
    elif config.use_metaphone_alg == "double":
        pair = doublemetaphone(s)
        return pair[0]

    # If we don't recognize metaphone algorithm, throw an exception.
    raise UnknownMetaphoneAlg("Did not recognize metaphone algoritm '%s'" % config.use_metaphone_alg)
