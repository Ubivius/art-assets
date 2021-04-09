import argparse
import cv2
from logger import logger
import utils
from PIL import Image
import numpy as np
from sklearn.metrics import mean_squared_error
import random


def get_best_matching_unit(codebook, vector_row):
    distances = list()
    for codebook_row in codebook:
        dist = utils.euclidean_distance(codebook_row, vector_row)
        distances.append(dist)
    return np.nanargmin(distances)


def train_codebook(vectors, codebook):
    mse = -1
    is_not_done = True
    while is_not_done:
        new_codebook = np.array(codebook)
        hit_counter = np.zeros((len(codebook), 1))

        encoded = np.zeros(len(vectors))
        decoded = np.zeros((len(vectors), len(vectors[0])))

        for i, vector in enumerate(vectors):
            bmu = get_best_matching_unit(codebook, vector)
            encoded[i] = bmu
            hit_counter[bmu] = hit_counter[bmu] + 1
            new_codebook[bmu] = new_codebook[bmu] + vectors[i]

        for i, row in enumerate(new_codebook):
            new_codebook[i, 0] = int(row[0] / hit_counter[i])
            new_codebook[i, 1] = int(row[1] / hit_counter[i])

        for i, row in enumerate(encoded):
            decoded[i, 0] = new_codebook[int(row), 0]
            decoded[i, 1] = new_codebook[int(row), 1]

        new_mse = mean_squared_error(vectors, decoded)
        print(new_mse)
        if mse != -1 and new_mse >= mse:
            is_not_done = False
        else:
            codebook = new_codebook
            mse = new_mse
    return codebook


def v_encode(codebook, vectors):
    encoded = np.zeros(len(vectors))
    for i, vector in enumerate(vectors):
        encoded[i] = get_best_matching_unit(codebook, vector)
    return encoded


def v_decode(codebook, vectors):
    o_vectors = np.zeros((len(vectors), 2))
    for i, vector in enumerate(vectors):
        index = int(vector)
        o_vectors[i, 0] = codebook[index, 0]
        o_vectors[i, 1] = codebook[index, 1]
    return o_vectors


def main(args):
    i_source = cv2.imread(args.image)
    i_height, i_width, i_channel = i_source.shape

    bit_budget = int(args.bits)

    logger.info("- Informations -----------------------------")
    logger.info(f"Image          : {args.image}")
    logger.info(f"Size           : {i_height} x {i_width}")
    logger.info(f"Bit budget     : {args.bits} bits")

    reduced_width = int(args.width)
    reduced_height = int(reduced_width * i_height / i_width)

    i_source = cv2.resize(i_source, (reduced_width, reduced_height))

    if args.gray:
        i_source = cv2.cvtColor(i_source, cv2.COLOR_RGB2GRAY)

        cv2.imshow("Grayscale", i_source)

    v_height = int(reduced_height * reduced_width / 2)
    v_width = 2
    i_vectors = i_source.reshape((v_height, v_width))
    codebook = utils.init_codebook("equal", bit_budget, 2)
    codebook = train_codebook(i_vectors, codebook)
    encoded = v_encode(codebook, i_vectors)
    o_vectors = v_decode(codebook, encoded)
    decoded = o_vectors.reshape((reduced_height, reduced_width))

    print(codebook)
    cv2.imwrite("./output.png", decoded)
    cv2.imshow("Pixel Art", decoded/255)
    cv2.waitKey()

# Command
# python main.py -i ./dessin1.jpg -n 2 -w 256 -g

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A script generate pixel art from full size picture"
    )
    parser.add_argument("-i", "--image", required=True, help="Path to the input image")
    parser.add_argument("-n", "--bits", required=True, help="Amount of bits used by the quantifier")
    parser.add_argument("-w", "--width", required=True, help="Image output width")
    parser.add_argument("-g", "--gray", const=True, default=False, nargs="?", help="Output the result in grayscale")

    args = parser.parse_args()

    main(args)
