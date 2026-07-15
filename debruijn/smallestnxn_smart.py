# V3 from locked, solving optimal 3x3

# import PIL
from PIL import Image
import math
import numpy as np
import random
import heapq
from multiprocessing import Process

size = 3

num_images = 2 ** (size * size)
width = 2 ** math.floor((size * size) / 2)
height = 2 ** math.ceil((size * size) / 2)
print(width * size, height * size)

#1 black, 2 white
# negative means "essential"

def score(img):
    ids = set()
    for r in range(len(img) - size + 1):
        for c in range(len(img[0]) - size + 1):
            id = 0
            i = 0
            for dr in range(size):
                for dc in range(size):
                    id += (0 if abs(img[r + dr][c + dc]) == 1 else 1) << i
                    i += 1
            original_size = len(ids)
            ids.add(id)
    return len(ids) / num_images

def score_new(img):
    ids = set()
    cols = [0] * 16
    for r in range(len(img) - size + 1):
        for c in range(len(img[0]) - size + 1):
            cols[c] += get_id(img, r, c)
    s = 0
    for c in cols:
        s += 8176 - abs(8176 - c)
    return s / 130816

def get_id(img, r, c):
    id = 0
    i = 0
    for dr in range(size):
        for dc in range(size):
            id += (0 if abs(img[r + dr][c + dc]) == 1 else 1) << i
            i += 1
    return id

def get_id_for_img(img):
    id = 0
    i = 0
    for r in range(len(img)):
        for c in range(len(img[0])):
            id += (0 if abs(img[r][c]) == 1 else 1) << i
            i += 1
    return id

def histogram(img):
    histo = [0] * num_images
    for r in range(len(img) - size + 1):
        for c in range(len(img[0]) - size + 1):
            histo[get_id(img, r, c)] += 1
    return histo

def histogram_img(img, histo):
    new_img = new(len(img[0]), len(img))
    for r in range(len(img) - size + 1):
        for c in range(len(img[0]) - size + 1):
            id = get_id(img, r, c)
            for dr in range(size):
                for dc in range(size):
                    new_img[r + dr][c + dc] *= histo[id] - 1
    return new_img

def histogram_mutate(img):
    histo = histogram(img)
    histo_img = histogram_img(img, histo)

    mutate_id = 0
    while histo[mutate_id] >= 1:
        mutate_id += 1

    for r in range(len(img) - size + 1):
        for c in range(len(img[0]) - size + 1):
            if histo_img[r][c] >= 1:
                for dr in range(size):
                    for dc in range(size):
                        img[r + dr][c + dc] = 2 if (mutate_id & 1) == 1 else 1
                        mutate_id = mutate_id >> 1
                return img

    # print("Didn't find anything replaceable")
    return img

# If the pixel is redundant, switch it to a square we don't already have
# This doesn't really make sense since it's not just that pixel that should be considered
def histogram_mutate(img):
    histo = histogram(img)
    histo_img = histogram_img(img, histo)

    mutate_id = 0
    while mutate_id < num_images and histo[mutate_id] >= 1:
        mutate_id += 1

    if mutate_id == num_images:
        return img

    for r in range(len(img) - size + 1):
        for c in range(len(img[0]) - size + 1):
            if histo_img[r][c] >= 1:
                for dr in range(size):
                    for dc in range(size):
                        img[r + dr][c + dc] = 2 if (mutate_id & 1) == 1 else 1
                        mutate_id = mutate_id >> 1
                return img

    # print("Didn't find anything replaceable")
    return img

# If the pixel is part of only redundant squares, flip it
def histogram_pixel_flip_mutate(img, flips=1):
    histo_img = histogram_img(img, histogram(img))

    choices = []

    for r in range(len(img)):
        for c in range(len(img[0])):
            if histo_img[r][c] >= 1:
                choices.append((r, c))
    
    for r, c in random.choices(choices, k=min(flips, len(choices))):
        img[r][c] = 2 if img[r][c] == 1 else 1

    # print("Didn't find anything replaceable")
    return img

# If all the pixels are for redundant squares, then switch them to square we don't already have
def histogram_precise_mutate(img):
    histo = histogram(img)
    histo_img = histogram_img(img, histo)

    mutate_id = 0
    while mutate_id < num_images and histo[mutate_id] >= 1:
        mutate_id += 1

    if mutate_id == num_images:
        return img

    for r in range(len(img) - size + 1):
        for c in range(len(img[0]) - size + 1):
            n = 1
            for dr in range(size):
                for dc in range(size):
                     n *= histo_img[r + dr][c + dc]

            if n >= 1:
                for dr in range(size):
                    for dc in range(size):
                        img[r + dr][c + dc] = 2 if (mutate_id & 1) == 1 else 1
                        mutate_id = mutate_id >> 1
                return img

    # print("Didn't find anything replaceable")
    return img

def histogram_flip_mutate(img, flips=1):
    for _ in range(flips):
        histo = histogram(img)

        mutate_id = 0
        while mutate_id < num_images and histo[mutate_id] >= 1:
            mutate_id += 1

        if mutate_id == num_images:
            return img

        r = random.randint(0, len(img) - size)
        c = random.randint(0, len(img[0]) - size)
        for dr in range(size):
            for dc in range(size):
                img[r + dr][c + dc] = 2 if (mutate_id & 1) == 1 else 1
                mutate_id = mutate_id >> 1
        return img

    return img

def new(w, h):
    return [[1] * (w) for i in range(h)]

def new_random(w, h):
    new_img = new(w, h)
    for r in range(len(new_img)):
        for c in range(len(new_img[0])):
            new_img[r][c] = random.randint(1, 2)
    return new_img

def new_checkerboard(w, h):
    new_img = new(w, h)
    for r in range(len(new_img)):
        for c in range(len(new_img[0])):
            new_img[r][c] = ((r + c) % 2) + 1 # random.randint(1, 2)
    return new_img

def copy(img):
    new = []
    for r in range(len(img)):
        new.append(img[r][:])
    return new

def mutate(img, flips=200, lock=True):
    for _ in range(flips):
        r = random.randint(0, len(img) - 1)
        c = random.randint(0, len(img[0]) - 1)
        if img[r][c] > 0 or not lock:
            img[r][c] = 2 if img[r][c] == 1 else 1
    return img

def merge(img1, img2):
    new_img = copy(img1)
    for r in range(len(img1)):
        for c in range(len(img1[0])):
            if random.randint(0, 1) == 0:
                new_img[r][c] = abs(img1[r][c])
            else:
                new_img[r][c] = abs(img2[r][c])
    return new_img

def merge_locks(img1, img2):
    new_img = copy(img1)
    for r in range(len(img1)):
        for c in range(len(img1[0])):
            if img1[r][c] < 0:
                new_img[r][c] = img1[r][c]
            elif img2[r][c] < 0:
                new_img[r][c] = img2[r][c]
            elif random.randint(0, 1) == 0:
                new_img[r][c] = img1[r][c]
            else:
                new_img[r][c] = img2[r][c]
    return new_img

def shrink(img, new_w, new_h):
    new_img = new(new_w, new_h)
    for r in range(new_h):
        for c in range(new_w):
            new_img[r][c] = abs(img[r][c])
    return new_img

def save(img, name):
    for r in range(len(img)):
        for c in range(len(img[0])):
            img[r][c] = abs(img[r][c]) == 1

    img = np.asarray(img)

    png_img = Image.fromarray(img)
    png_img = png_img.convert("L")
    print("saving " + name)
    png_img.save(name + '.png', bits=1, optimize=True)

def run():
    last_best = None
    curr_width, curr_height = 18, 34#width * size, height * size
    for step in range(1000):
        running = True
        
        # print(step)
        # if (step + 1) % 10 == 0:
            # save(last_best, str(step))

        population = [new_random(curr_width, curr_height) for _ in range(20)]
        while running:
            optimal = False
            curr_best_score = -1
            curr_best_score_num = 0
            x = 0
            while curr_best_score_num < 400:
                rank = []
                for img in population:
                    heapq.heappush(rank, (-(score_new(img) * score(img)), img))

                top_rank = -rank[0][0]
                if rank[0][0] == -1: #-1:
                    print(rank[0][1])
                    save(rank[0][1], str(curr_width) + "x" + str(curr_height))
                    curr_width -= 1
                    curr_height -= 1
                    optimal = True
                    break

                if curr_best_score == top_rank:
                    curr_best_score_num += 1
                else:
                    curr_best_score_num = 0
                    curr_best_score = top_rank

                # if curr_best_score_num == 399:
                print(-rank[0][0], curr_best_score_num, curr_width, curr_height)
                
                crossable_population = 5
                population = []
                seen = set()
                while rank and len(population) < crossable_population:
                    img = heapq.heappop(rank)[1]
                    id = get_id_for_img(img)
                    if id in seen:
                        continue
                    seen.add(id)
                    population.append(img)
                crossable_population = len(population)

                # for _ in range(len(rank) - 5):
                    # heapq.heappop(rank)

                # while rank:
                    # population.append(heapq.heappop(rank)[1])

                # population.append(new_random(curr_width, curr_height))

                if last_best and curr_best_score_num > 250:
                    population.append(last_best)
                    crossable_population += 1
                    last_best = None
                    print("Releasing the Kraken")

                for i in range(crossable_population):
                    # Basic flips
                    population.append(mutate(copy(population[i]), flips = 1))
                    population.append(mutate(copy(population[i]), flips = 10 + 1 * x))
                    # Histogram flips
                    population.append(histogram_flip_mutate(copy(population[i])))
                    population.append(histogram_pixel_flip_mutate(histogram_flip_mutate(copy(population[i])), flips=10))
                    population.append(histogram_flip_mutate(copy(population[i]), flips=3))
                    # Cleanup histogram flips
                    population.append(histogram_pixel_flip_mutate(copy(population[i]), flips=1))
                    population.append(histogram_pixel_flip_mutate(copy(population[i]), flips=100))
                    population.append(histogram_pixel_flip_mutate(histogram_precise_mutate(copy(population[i])), flips=5))

                if crossable_population > 1:
                    for _ in range(10):
                        i = 0
                        j = 0
                        while i == j:
                            i = random.randint(0, crossable_population - 1)
                            j = random.randint(0, crossable_population - 1)
                        population.append(merge(population[i], population[j]))

                # for _ in range(5):
                    # i = 0
                    # j = 0
                    # while i == j:
                        # i = random.randint(0, crossable_population - 1)
                        # j = random.randint(0, crossable_population - 1)
                    # population.append(mutate(merge(population[i], population[j]), flips = 10 + 5 * x))
                x += 1
            # population = [shrink(img, curr_width, curr_height) for img in population]
            last_best = population[0]
            running = optimal

# if __name__ == '__main__':
    # for i in range(2):
        # p = Process(target=run)
        # p.start()

# value = [[1, 2, 1, 2, 1, 2, 2, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 2], [2, 2, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2], [1, 2, 1, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 1, 2, 2, 2, 2, 1], [1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1], [2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 2, 1], [2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1], [1, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2], [1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 1, 1, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 2, 2], [2, 2, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1], [2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 1, 2, 2], [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 2], [2, 2, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1], [1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 2], [2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2], [2, 2, 2, 2, 1, 2, 2, 1, 1, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 2, 1], [2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1, 1, 1], [1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 2, 2, 1, 2, 1, 1], [2, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2], [2, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 2, 2, 1, 2, 1], [2, 2, 1, 1, 1, 2, 2, 2, 1, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1], [2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 1], [1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1], [2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1], [2, 2, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 2, 1, 1], [2, 2, 1, 2, 1, 2, 2, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2], [1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2], [2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 2, 2, 1, 2, 1, 1, 1, 2, 2, 2, 1, 1, 1], [1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2], [1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1, 2, 1], [1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 1, 2, 2, 2, 1, 2], [1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2], [2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1, 2, 1], [2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2], [2, 2, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 1]]

# ones = 0
# twos = 0
# for r in range(len(value)):
    # for c in range(len(value[0])):
        # if value[r][c] == 1:
            # ones += 1
        # elif value[r][c] == 2:
            # twos += 1
# print(ones, twos)
# save(value, "25x34")

run()

print("done")



