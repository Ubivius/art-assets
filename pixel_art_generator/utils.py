import math
import numpy as np
from logger import logger


def euclidean_distance(row1, row2):
    """ Method that process the Euclidean distance between two vectors

    :param row1: First vector
    :param row2: Second vector
    :return: Euclidean distance
    """
    #distance = 0.0
    #for i in range(len(row1)-1):
    #    distance += (row1[i] - row2[i])**2
    #np.sum(row1 - row2) ** 2
    return np.sqrt((row1 - row2).sum() ** 2)


def init_codebook(init_type, N, width):
    """ Initialisation of the codebook

    :param init_type: Type of initialisation
    :param N: Bit budget
    :return: Initialized codebook
    """
    codebook = np.zeros((2 ** N, width))
    if init_type == "random":
        pass
    elif init_type == "equal":
        for i in range(0, 2 ** N):
            for j in range(0, width):
                codebook[i, j] = (256 / 2 ** N) * (i + 1) - 1
    elif init_type == "fixed":
        codebook = np.array([[27, 27],
                             [101, 101],
                             [175, 175],
                             [216, 216]])
    else:
        logger.error("Wrong type of codebook initialisation. Try \"equal\" or \"random\".")
    return codebook

