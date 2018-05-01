import numpy as np
from numpy import dot
from numpy.linalg import norm


def cosine_similarity(a, b):
    return dot(a, b)/(norm(a)*norm(b))

a = np.random.rand(5000000)
b = np.random.rand(5000000)
print(cosine_similarity(a, b))
