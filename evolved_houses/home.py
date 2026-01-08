import random
import matplotlib.pyplot as plt
import numpy as np
import render_house as render
import math

def random_house():
    house = []
    for y in range(5):
        x_dim = []
        for x in range(10):
            z_dim = []
            for z in range(10):
                flip = random.randint(0, 1)
                flip2  = random.randint(0, 1)
                z_dim.append(flip == 1 and flip2 == 1)
            x_dim.append(z_dim)
        house.append(x_dim)
    return house
    
def perfect_house():
    house = []
    for y in range(5):
        x_dim = []
        for x in range(10):
            z_dim = []
            for z in range(10):
                z_dim.append((y == 2) or (x == 0 and z == 0 and y < 3))
            x_dim.append(z_dim)
        house.append(x_dim)
    return house
    
def pyramid_roof(height=5):
    house = []
    for y in range(5):
        x_dim = []
        for x in range(10):
            z_dim = []
            for z in range(10):
                # y2 = 4 - y
                y2 = y
                z_dim.append(y2 < height and x >= 0 + y2 and x <= 9 - y2 and z >= 0 + y2 and z <= 9 - y2)
            x_dim.append(z_dim)
        house.append(x_dim)
    return house
    
def ball(radius=5):
    house = []
    for y in range(int(radius * 2 + 1)):
        x_dim = []
        for x in range(int(radius * 2 + 1)):
            z_dim = []
            for z in range(int(radius * 2 + 1)):
                distance = math.sqrt((y - radius) ** 2 + (x - radius) ** 2 + (z - radius) ** 2)
                z_dim.append(distance <= radius)
            x_dim.append(z_dim)
        house.append(x_dim)
    return house
    
def globe(radius=5, gap=30):
    house = empty_house(radius * 2 + 1)

    x = radius
    y = radius
    z = 0
    for theta in range(360 // gap):
        for phi in range(360):
            pass

    return house

def empty_house(height = 5):
    house = []
    for y in range(height):
        x_dim = []
        for x in range(10):
            z_dim = []
            for z in range(10):
                z_dim.append(False)
            x_dim.append(z_dim)
        house.append(x_dim)
    return house
    
def fresh_height_map():
    x_dim = []
    for x in range(10):
        z_dim = []
        for z in range(10):
            z_dim.append(0)
        x_dim.append(z_dim)
    return x_dim
    
def get_height_map_for_house(house):
    ans = fresh_height_map()
    for y in range(5):
        for x in range(10):
            for z in range(10):
                val = house[y][x][z]
                if val:
                    ans[x][z] = y + 1
    return ans

def structural_adjacencies(pos):
    x, y, z = pos
    adj = [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]
    adj = list(filter(lambda t: t[0] >= 0 and t[0] < 10 and t[1] >= 0 and t[1] < 5 and t[2] >= 0 and t[2] < 10, adj))
    return adj
    
def horizontal_adjacencies(pos):
    x, y, z = pos
    adj = [(x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1)]
    adj = list(filter(lambda t: t[0] >= 0 and t[0] < 10 and t[2] >= 0 and t[2] < 10, adj))
    return adj
    
def physics_normalize_house(house):
    normalizations = 0
    valid_house = empty_house()
    normalized_house = empty_house()
    height_map = fresh_height_map()
    
    # print("pre-normalized house", sum(sum(x.count(True) for x in y) for y in house))

    for y in range(5):
        for x in range(10):
            for z in range(10):
                val = house[y][x][z]
                if y == 0 and val:
                    valid_house[y][x][z] = True
                    height_map[x][z] = 1
                elif val and valid_house[y - 1][x][z] and not valid_house[y][x][z]:
                    valid_house[y][x][z] = True
                    height_map[x][z] = y + 1
                    q = horizontal_adjacencies((x, y, z))
                    while q:
                        xa, ya, za = q.pop()
                        vala = house[ya][xa][za]
                        if vala and not valid_house[ya][xa][za]:
                            valid_house[ya][xa][za] = True
                            height_map[x][z] = y + 1
                            q.extend(horizontal_adjacencies((xa, ya, za)))
        for x in range(10):
            for z in range(10):
                normalized_house[y][x][z] = valid_house[y][x][z]
                if house[y][x][z] and not valid_house[y][x][z]:
                    # normalized_house[y][x][z] = house[y][x][z]
                    normalizations += 1
                    height = height_map[x][z]
                    while normalized_house[height][x][z]:
                        height += 1
                    normalized_house[height][x][z] = True
                    height_map[x][z] = height + 1

    # print("orig", sum(sum(x.count(True) for x in y) for y in house))
    # print("normalized", sum(sum(x.count(True) for x in y) for y in normalized_house))

    return normalized_house
    
def physics_normalize_roof(house):
    normalized_house = empty_house()
    height_map = fresh_height_map()
    
    # print("pre-normalized house", sum(sum(x.count(True) for x in y) for y in house))

    for y in range(5):
        for x in range(10):
            for z in range(10):
                if house[y][x][z]:
                    normalized_house[height_map[x][z]][x][z] = True
                    height_map[x][z] += 1

    # print("orig", sum(sum(x.count(True) for x in y) for y in house))
    # print("normalized", sum(sum(x.count(True) for x in y) for y in normalized_house))

    return normalized_house

def plot_house(house):
    xs = []
    ys = []
    zs = []
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if house[y][x][z]:
                    xs.append(x)
                    ys.append(y)
                    zs.append(z)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(
           xs,
           zs,
           ys)
    plt.show()
    
def plot_house_voxels(house):
    fig = plt.figure()

    house = np.array(house)
    house = np.swapaxes(house, 0, 2)
    
    ax = fig.gca(projection='3d')
    ax.voxels(house, edgecolor='k')

def show_plots():
    plt.show() 
    
### Eval funcs for entire house
def protection_eval_func(house):
    prot_map = fresh_height_map()
    for y in range(3):
        for x in range(10):
            for z in range(10):
                if house[y + 2][x][z]:
                    prot_map[x][z] = 1
    return sum(x.count(1) for x in prot_map)

def space_eval_func(house):
    blocked_map = fresh_height_map()
    for y in range(2):
        for x in range(10):
            for z in range(10):
                if house[y][x][z]:
                    blocked_map[x][z] = 1
    return sum(x.count(0) for x in blocked_map)

def economy_eval_func(house):
    return sum(sum(x.count(False) for x in y) for y in house) / 5.0
    
def eval_func(house):
    return (2 * protection_eval_func(house) + 1 * space_eval_func(house) + 1 * economy_eval_func(house)) / 4.0

### Genetic for entire house
def generate_initial_population(n = 50):
    population = []
    for i in range(n):
        house = random_house()
        house = physics_normalize_house(house)
        population.append(house)
    return population

def crossover_houses(h1, h2):
    house = empty_house()
    for y in range(5):
        for x in range(10):
            for z in range(10):
                flip = random.randint(0, 1)
                if flip == 0:
                    house[y][x][z] = h1[y][x][z]
                else:
                    house[y][x][z] = h2[y][x][z]
    return physics_normalize_house(house)
    
def crossover_houses_by_layer(h1, h2):
    house = empty_house()
    for y in range(5):
        flip = random.randint(0, 1)
        for x in range(10):
            for z in range(10):
                if flip == 0:
                    house[y][x][z] = h1[y][x][z]
                else:
                    house[y][x][z] = h2[y][x][z]
    return physics_normalize_house(house)

def mutate_house(house):
    for y in range(5):
        for x in range(10):
            for z in range(10):
                flip = random.randint(0, 50)
                if flip == 0:
                    house[y][x][z] = not house[y][x][z]
    return physics_normalize_house(house)
    
def mutate_house_by_layer(house):
    for y in range(5):
        flip = random.randint(0, 4)
        for x in range(10):
            for z in range(10):
                if flip == 0:
                    house[y][x][z] = True # not house[y][x][z]

    flip = random.randint(0, 19)
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if x == flip:
                    house[y][x][z] = True # not house[y][x][z]

    flip = random.randint(0, 19)
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if z == flip:
                    house[y][x][z] = True #not house[y][x][z]

    for y in range(5):
        for x in range(10):
            for z in range(10):
                flip = random.randint(0, 20)
                if flip == 0:
                    house[y][x][z] = False                  

    return physics_normalize_house(house)
    
def mutate_house_by_line(house):
    flip = random.randint(0, 10)
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if x == flip and y == flip:
                    house[y][x][z] = True #not house[y][x][z]

    flip = random.randint(0, 10)
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if x == flip and z == flip:
                    house[y][x][z] = True #not house[y][x][z]

    flip = random.randint(0, 10)
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if y == flip and z == flip:
                    house[y][x][z] = True #not house[y][x][z]
    return physics_normalize_house(house)

def get_n_best(population, eval_function=eval_func, n = 10, print_eval = False):
    evals = []
    for house in population:
        evals.append(eval_function(house))
    sorted_evals, sorted_pop = (list(t) for t in zip(*sorted(zip(evals, population), reverse=True)))
    if print_eval:
        print(sorted_evals)
    kept_houses = sorted_pop[0:n]
    return kept_houses

def cut_and_refill_population(population, n = 100, keepers = 10, eval_function=eval_func, mutation_func=mutate_house_by_layer, crossover_func=crossover_houses_by_layer):
    kept_houses = get_n_best(population, eval_function=eval_function, n = keepers)
    new_houses = []
    for i in range(n - keepers):
        k1 = random.randint(0, keepers - 1)
        k2 = random.randint(0, keepers - 1)
        while k1 == k2:
            k2 = random.randint(0, keepers - 1)
    
        h1 = kept_houses[k1]
        h2 = kept_houses[k2]
        new_houses.append(crossover_func(h1, h2))
    for house in new_houses:
        kept_houses.append(mutation_func(house))
    return kept_houses
    
def run(runs = 50):
    pop = generate_initial_population()
    for i in range(runs):
        pop = cut_and_refill_population(pop)
    best = get_n_best(pop, n=1, print_eval=True)[0]
    plot_house_voxels(best)
    show_plots()
    
### Eval funcs for walls and roof
def roof_sun_protection_eval_func(house):
    prot_map = fresh_height_map()
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if house[y][x][z]:
                    prot_map[x][z] = 1
    return sum(x.count(1) for x in prot_map)

def roof_water_protection_eval_func(house):
    height_map = get_height_map_for_house(house)
    
    ans = 0.0
    for x in range(10):
        for z in range(10):
            if height_map[x][z] == 0:
                ans += 1.0
                continue
        
            locs = [(x, z, 1.0)]
            while locs:
                xc, zc, score = locs.pop()
                yc = height_map[xc][zc]
                if xc == 0 or xc == 9 or zc == 0 or zc == 9 or yc == 0:
                    ans += score
                    continue
                adjs = horizontal_adjacencies((xc, 0, zc))
                valid_adjs = []
                for adj in adjs:
                    xa, _, za = adj
                    ya = height_map[xa][za]
                    if ya < yc:
                        valid_adjs.append((xa, za))
                num = len(valid_adjs)
                for adj in valid_adjs:
                    xa, za = adj
                    locs.append((xa, za, score / num))

    return ans
    
def x_symmetry_eval_func(house):
    score = 0
    for y in range(5):
        for x in range(5):
            for z in range(10):
                if house[y][x][z] == house[y][9 - x][z]:
                    score += 2.0
    return score / 5.0
    
def z_symmetry_eval_func(house):
    score = 0
    for y in range(5):
        for x in range(10):
            for z in range(5):
                if house[y][x][z] == house[y][x][9 - z]:
                    score += 2.0
    return score / 5.0
    
def material_sweetspot_eval_func(house, sweetspot):
    economy = 100 - economy_eval_func(house)
    max_delta = max(100 - sweetspot, sweetspot)
    return 100 * (100 - abs(sweetspot - economy)) / max_delta
    
def high_roof_eval_func(house):
    score = 0
    for x in range(10):
        for z in range(10):
            if house[4][x][z]:
                score += 1.0
    return score

def wall_space_eval_func(house):
    blocked_map = fresh_height_map()
    for y in range(2):
        for x in range(10):
            for z in range(10):
                if house[y][x][z]:
                    blocked_map[x][z] = 1
    return sum(x.count(0) for x in blocked_map)
    
def wall_support_eval_func(house):
    for y in range(4):
        for x in range(10):
            for z in range(10):
                if house[y + 1][x][z]:
                    return 100
    return 0
    
def roof_eval_func(house):
    return (1 * roof_sun_protection_eval_func(house) + 0.03 * roof_water_protection_eval_func(house) + 0.0 * material_sweetspot_eval_func(house, 46) + 0.3 * (1 / x_symmetry_eval_func(house)) + 0.6 * z_symmetry_eval_func(house)) / 300.0

def wall_eval_func(house):
    return (1 * wall_space_eval_func(house) + 1 * wall_support_eval_func(house) + 1 * economy_eval_func(house)) / 3.0

### Genetic for walls and roof
def generate_initial_population_of_roofs(n = 50):
    population = []
    for i in range(n):
        house = empty_house()
        house = physics_normalize_roof(house)
        population.append(house)
    return population

def generate_initial_population_of_walls(n = 50):
    population = []
    for i in range(n):
        house = empty_house()
        house = physics_normalize_house(house)
        population.append(house)
    return population
    
def crossover_roofs(h1, h2):
    house = empty_house()
    for y in range(5):
        flip = random.randint(0, 1)
        for x in range(10):
            for z in range(10):
                if flip == 0:
                    house[y][x][z] = h1[y][x][z]
                else:
                    house[y][x][z] = h2[y][x][z]
    return physics_normalize_roof(house)
    
def crossover_walls(h1, h2):
    house = empty_house()
    for y in range(5):
        flip = random.randint(0, 1)
        for x in range(10):
            for z in range(10):
                if flip == 0:
                    house[y][x][z] = h1[y][x][z]
                else:
                    house[y][x][z] = h2[y][x][z]
    return physics_normalize_house(house)

def uniform_random_range():
    a = random.randint(0, 9)
    b = random.randint(0, 9)
    if a > b:
        return (b, a)
    else:
        return (a, b)

def mutate_roof_by_layer(house):
    # flip_z_line = random.randint(0, 19)
    # flip_y_line = random.randint(0, 19)
    # flip_x_line = random.randint(0, 19)
    for y in range(5):
        delete_layer = random.randint(0, 5)
        flip_y_plane = random.randint(0, 5)
        start_x, end_x = uniform_random_range()
        start_z, end_z = uniform_random_range()
        for x in range(10):
            for z in range(10):
                if flip_y_plane == 0 and x >= start_x and x <= end_x and z >= start_z and z <= end_z:
                    house[y][x][z] = True # not house[y][x][z]
                    
                if delete_layer == 0:
                    house[y][x][z] = False
                # if x == flip_z_line and y == flip_z_line:
                    # house[y][x][z] = not house[y][x][z]
                # if x == flip_y_line and z == flip_y_line:
                    # house[y][x][z] = not house[y][x][z]
                # if y == flip_x_line and z == flip_x_line:
                    # house[y][x][z] = not house[y][x][z]
                # if flip_point == 0:
                    # house[y][x][z] = not house[y][x][z]

    return physics_normalize_roof(house)
    
def mutate_walls_by_layer(house):
    flip = random.randint(0, 19)
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if x == flip:
                    house[y][x][z] = not house[y][x][z]

    flip = random.randint(0, 19)
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if z == flip:
                    house[y][x][z] = not house[y][x][z]

    flip = random.randint(0, 19)
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if x == flip and y == flip:
                    house[y][x][z] = not house[y][x][z]

    flip = random.randint(0, 19)
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if x == flip and z == flip:
                    house[y][x][z] = not house[y][x][z]

    flip = random.randint(0, 19)
    for y in range(5):
        for x in range(10):
            for z in range(10):
                if y == flip and z == flip:
                    house[y][x][z] = not house[y][x][z]
    return physics_normalize_house(house)
    
def run_parted(runs = 50):
    pop = generate_initial_population_of_roofs()
    
    ## Walls
    # for i in range(runs):
        # pop = generate_initial_population_of_walls()
        # pop = cut_and_refill_population(pop, eval_function=wall_eval_func, mutation_func=mutate_walls_by_layer, crossover_func=crossover_walls)
    # best = get_n_best(pop, n=1, eval_function=wall_eval_func, print_eval=True)[0]
    # plot_house_voxels(best)
    
    ## Roofs
    for i in range(runs):
        pop = cut_and_refill_population(pop, n=100, keepers=10, eval_function=roof_eval_func, mutation_func=mutate_roof_by_layer, crossover_func=crossover_roofs)
    best = get_n_best(pop, n=5, eval_function=roof_eval_func, print_eval=True)
    
    for i in range(1):
        print(material_sweetspot_eval_func(best[i], 0))
        plot_house_voxels(best[i])

    show_plots()
    return best[0]

if __name__ == "__main__":
    # roof = pyramid_roof(height=5)
    # roof = physics_normalize_roof(roof)
    # print(roof_water_protection_eval_func(roof))
    # plot_house_voxels(roof)
    # show_plots()
    
    ## HOUSE SIM
    # house = run_parted(500)
    # plot_house_voxels(house)
    # show_plots()
    
    
    ## ROOF SIM
    best_roof = run_parted(1000)
    # best_roof = pyramid_roof()
    height_map = get_height_map_for_house(best_roof)
    house = empty_house(height=10)
    for x in range(10):
        for z in range(10):
            if height_map[x][z] > 0:
                surrounded = True
                for adj in horizontal_adjacencies((x, 0, z)):
                    xa, _, za = adj
                    if height_map[xa][za] == 0 or x == 0 or z == 0 or x == 9 or z == 9:
                        surrounded = False
                        break
                for y in range(3):
                    house[y][x][z] = surrounded
                for y in range(5):
                    y2 = y + 3
                    house[y2][x][z] = best_roof[y][x][z]

    # plot_house_voxels(house)
    # show_plots()
    
    # house = empty_house(height=10)
    # house[0][0][0] = True
    # house = ball(25)
    
    poly3d = render.get_3d_polygons_for_house(house)
    # poly3d = render.get_3d_polygons_for_sphere()
    # poly3d = render.get_3d_polygons_for_car()
    render.render_poly3d(poly3d)
    
    # house = empty_house()
    # for i in range(20):
        # house = mutate_roof_by_layer(house)
        # print(roof_water_protection_eval_func(house))
        # plot_house_voxels(house)
        # show_plots()
        
        
    
    # house = physics_normalize_house(empty_house())
    # print(eval_func(house))
    # plot_house_voxels(house)
    # show_plots()
    
    # house = random_house()
    # norm_house = physics_normalize_house(house)
    # # print(house)
    # # print(norm_house)
    # plot_house_voxels(house)
    # plot_house_voxels(norm_house)
    # print(protection_eval_func(house))
    # print(space_eval_func(norm_house))
    # print(economy_eval_func(norm_house))
    # show_plots()