import cv2
import numpy as np
from PIL import Image, ImageOps


print("Pixel Art Generator")
bit_budget = 2
i_path = "./dessin1.jpg"
is_gray = False

i_source = cv2.imread(i_path)
i_height, i_width, i_channel = i_source.shape



reduced_height = 256
reduced_width = int(reduced_height * i_width / i_height)

print(i_source.shape)

print("- Informations -----------------------------")
print(f"Image          : {i_path}")
print(f"Size           : {i_height} x {i_width}")
print(f"Bit budget     : {bit_budget} bits")



i_gray = cv2.cvtColor(i_source, cv2.COLOR_BGR2GRAY)
i_gray = cv2.resize(i_gray, (reduced_width, reduced_height))
i_source = cv2.resize(i_gray, (reduced_width, reduced_height))
g_height, g_width = i_gray.shape



v_height = int(g_height * g_width / 2)
v_width = 2

# Codebook creation
codebook = np.zeros((2 ** bit_budget, 2))
for i in range(0, 2 ** bit_budget):
    codebook[i, 0] = (256 / 2 ** bit_budget) * (i + 1) - 1
    codebook[i, 1] = 128

print(codebook)
c_height, c_width = codebook.shape

i_vectors = i_gray.reshape((v_height, v_width))

it_counter = 0
i_encoded = []
while it_counter <= 10:
    new_codebook = np.zeros((c_height, c_width))
    new_i_encoded = np.zeros((v_height, 1))
    hit_counter = np.zeros((c_height, 1))

    if not is_gray:
        for i in range(v_height):
            dist = np.zeros((4, 1))

            for j in range(0, c_height):
                dist[j] = np.sqrt(sum((i_vectors[j, ] - codebook[j, ]) ** 2))

            lowest_index = np.argmin(dist)
            new_i_encoded[i] = lowest_index
            hit_counter[lowest_index] = hit_counter[lowest_index] + 1
            new_codebook[lowest_index, ] = new_codebook[lowest_index, ] + i_vectors[i, ]
    else:
        pass
    for i in range(0, c_height):
        #print(codebook[i, 1] / hit_counter[i])
        codebook[i, 0] = int(codebook[i, 0] / hit_counter[i])
        codebook[i, 1] = int(codebook[i, 1] / hit_counter[i])
    it_counter += 1

    if it_counter <= 10:
        codebook = new_codebook
        i_encoded = new_i_encoded

o_vectors = np.zeros((v_height, v_width))
for i in range(0, v_height):
    o_vectors[i, 0] = codebook[i_encoded[i], 0];
    o_vectors[i, 1] = codebook[i_encoded[i], 1];

i_decoded = o_vectors.reshape((i_height, i_width))

cv2.imshow("Pixel Art", i_decoded)
cv2.waitKey()

