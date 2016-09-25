from math import *

_current_id = 0
def generate_id():
    global _current_id

    return _current_id


def length(vec):
    return sqrt(vec.x * vec.x + vec.y * vec.y)


def normalize(vec):
    return vec * (1.0 / length(vec))
