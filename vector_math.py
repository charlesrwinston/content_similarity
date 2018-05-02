import numpy as np
from numpy import dot
from numpy.linalg import norm


def cosine_similarity(a, b):
    return dot(a, b)/(norm(a)*norm(b))
