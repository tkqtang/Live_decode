import numpy as np
def add(x, y):
    return x + y


def test(data):
    data = np.array(data)
    if data.ndim == 1:
        data = data.reshape(1, -1)
    return data.shape