import PIL
from PIL import Image
import math
import numpy as np
import random
import heapq

size = 3

num_images = 2 ** (size * size)
width = 2 ** math.floor((size * size) / 2)
height = 2 ** math.ceil((size * size) / 2)

def score(img):
    ids = set()
    for r in range(len(img) - size + 1):
        for c in range(len(img[0]) - size + 1):
            id = 0
            i = 0
            for dr in range(size):
                for dc in range(size):
                    id += (0 if img[r + dr][c + dc] else 1) << i
                    i += 1
            ids.add(id)
    return len(ids) / num_images

def new(w, h):
    return [[False] * (w) for i in range(h)]

def copy(img):
    new = []
    for r in range(len(img)):
        new.append(img[r][:])
    return new

def mutate(img, flips=400):
    for _ in range(flips):
        r = random.randint(0, len(img) - 1)
        c = random.randint(0, len(img[0]) - 1)
        img[r][c] = not img[r][c]
    return img

def merge(img1, img2):
    new_img = copy(img1)
    for r in range(len(img)):
        for c in range(len(img[0])):
            if random.randint(0, 1) == 0:
                new_img[r][c] = img2[r][c]
    return new_img

def save(img, name):
    img = np.asarray(img)

    png_img = Image.fromarray(img)
    png_img = png_img.convert("L")
    print("saving " + name)
    png_img.save(name + '.png', bits=1, optimize=True)

curr_width, curr_height = 50, 50# width * size, height * size
running = True

while running:
    population = [new(curr_width, curr_height) for _ in range(20)]
    optimal = False
    for _ in range(10000):
        rank = []
        for img in population:
            heapq.heappush(rank, (-score(img), img))

        if rank[0][0] == -1:
            save(rank[0][1], str(curr_width) + "x" + str(curr_height))
            curr_width -= 1
            curr_height -= 1
            optimal = True
            break
        
        population = []
        for _ in range(5):
            population.append(heapq.heappop(rank)[1])

        for i in range(5):
            population.append(mutate(copy(population[i])))
            population.append(mutate(copy(population[i])))

        for _ in range(5):
            i = 0
            j = 0
            while i == j:
                i = random.randint(0, 4)
                j = random.randint(0, 4)
            population.append(merge(population[i], population[j]))
    running = optimal

print("done")



