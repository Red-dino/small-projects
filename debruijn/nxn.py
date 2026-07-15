import PIL
from PIL import Image
import math
import numpy as np

size = 6

num_images = 2 ** (size * size)
width = 2 ** math.floor((size * size) / 2)
height = 2 ** math.ceil((size * size) / 2)
print(num_images, width, height)

img = [[] for i in range(height * size)]

def get_image(id):
    row = size * (id // width)
    for dr in range(size):
        for _ in range(size):
            img[row + dr].append(id & 1 == 0)
            id = id >> 1

for i in range(num_images):
    get_image(i)

    if (i + 1) % 1000000 == 0:
        print(i)

img = np.asarray(img)

png_img = Image.fromarray(img)
png_img = png_img.convert("L")
png_img.save(str(size) + '.png', bits=1, optimize=True)

print("done")
