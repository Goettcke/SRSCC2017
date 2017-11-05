# EDIT configs/default.ini TO CHANGE SETTINGS
from config import config

import collections

_no_bytes_err = 'expected str, got bytes'


def damerau_levenshtein_distance(s1, s2):

    len1 = len(s1)
    len2 = len(s2)
    infinite = len1 + len2

    # character array
    da = collections.defaultdict(int)

    # distance matrix
    score = [[0] * (len2 + 2) for x in xrange(len1 + 2)]

    score[0][0] = infinite
    for i in xrange(0, len1 + 1):
        score[i + 1][0] = infinite
        score[i + 1][1] = i
    for i in xrange(0, len2 + 1):
        score[0][i + 1] = infinite
        score[1][i + 1] = i

    for i in xrange(1, len1 + 1):
        db = 0
        for j in xrange(1, len2 + 1):
            i1 = da[s2[j - 1]]
            j1 = db
            cost = 1
            if s1[i - 1] == s2[j - 1]:
                cost = 0
                db = j

            score[i + 1][j + 1] = min(score[i][j] + cost,
                                      score[i + 1][j] + 1,
                                      score[i][j + 1] + 1,
                                      score[i1][j1] + (i - i1 - 1) + 1 + (j - j1 - 1))
        da[s1[i - 1]] = i

    return score[len1 + 1][len2 + 1]


def percent_denominator(navn1,navn2):
    denominator = float(max(len(navn1), len(navn2)))
    if (denominator != 0):
        return denominator
    else :
        return 1.0 # To ensure we're not deviding by 0

def percent_levenshtein(navn1, navn2):
    return damerau_levenshtein_distance(navn1, navn2) / float(percent_denominator(navn1, navn2))

def percent_levenshtein_helper(navn1, navn2):
    if config.name_use_levenshtein:
        return percent_levenshtein(navn1, navn2)
    else:
        # If we don't use levenshtein, a exact match will have difference of 0 % 
        # and otherwise, it will have 100% difference.
        if navn1 == navn2:
            return 0.0
        else:
            return 1.0
