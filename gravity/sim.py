import math
import pygame
import random
import cProfile

class Particle:

    def __init__(self, x, y, m=1.0, v=(0, 0), r=2, fixed=False, tracker=False):
        self.x = x
        self.y = y
        self.v_x = v[0]
        self.v_y = v[1]
        self.a_x = 0
        self.a_y = 0
        self.m = m
        self.w = max(1, int(math.sqrt(m)))
        self.v_rotation = 0
        self.poly = (0, 0, 0, 0)

        self.radius = r

        self.f_x = 0
        self.f_y = 0

        self.fixed = fixed
        self.alive = True
        self.tracker = tracker

        self.recompute_color()

    def add_force(self, f_x, f_y):
        self.f_x += f_x
        self.f_y += f_y
        
    def resolve_forces(self):
        self.a_x = self.f_x / self.m
        self.a_y = self.f_y / self.m

        self.f_x = 0
        self.f_y = 0

    def update(self, t_step=1.0):
        self.resolve_forces()

        if not self.fixed:
            # update p
            self.x += self.v_x * t_step + 0.5 * self.a_x * t_step * t_step
            self.y += self.v_y * t_step + 0.5 * self.a_y * t_step * t_step

            # update v
            self.v_x += self.a_x * t_step
            self.v_y += self.a_y * t_step

    def recompute_color(self):
        if self.tracker:
            self.color = (200, 50, 50)
        else:
            self.color = (200, 200, max(0, 200 - self.m))

    def distance(p1, p2):
        x = p2.x - p1.x
        y = p2.y - p1.y
        return math.sqrt(x * x + y * y)

    def gravity(p1, p2):
        d = Particle.distance(p1, p2)
        
        if d == 0.0:
            return 0.0, 0.0

        x = (p2.x - p1.x) / d
        y = (p2.y - p1.y) / d

        f = 0.1 * p1.m * p2.m / (d * d)

        return f * x, f * y

    def collide(p1, p2):
        if p2.fixed or p2.m > p1.m:
            p1, p2 = p2, p1

        p1.tracker = p1.tracker or p2.tracker

        m_new = p1.m + p2.m
        v_x = (p1.v_x * p1.m + p2.v_x * p2.m) / m_new
        v_y = (p1.v_y * p1.m + p2.v_y * p2.m) / m_new

        p1.m = m_new
        p1.recompute_color()

        p1.v_x = v_x
        p1.v_y = v_y

        area = math.pow(2 * p1.radius, 2) + math.pow(2 * p2.radius, 2)

        p1.radius = math.sqrt(area) / 2

        p2.m = 0.0001
        p2.x = -10000000
        p2.y = -10000000
        p2.alive = False

class Generator:

    def generate_rotating_disk(n=10, center=(0, 0), d_range=(100, 500), m=3000.0, include_sun=True):

        particles = []
        for _ in range(n):
            angle = random.uniform(-math.pi, math.pi)
            x_unit = math.cos(angle)
            y_unit = math.sin(angle)

            # d = random.uniform(d_range[0], d_range[1])
            d = (d_range[1] - d_range[0]) * math.sqrt(random.uniform(0.0, 1.0)) + d_range[0]

            x = center[0] + x_unit * d
            y = center[1] + y_unit * d

            # sqrt(Gm/r)
            speed = random.uniform(0, 2.0)
            # speed = math.sqrt(0.1 * m / d)
            v_x = -y_unit * speed
            v_y = x_unit * speed

            gas = bool(random.getrandbits(1))
            mass = 10.0 if gas else 50.0
            r = 5.0 if gas else 2.0

            particles.append(Particle(x, y, v=(v_x, v_y), m=mass, r=r))

        if include_sun:
            particles.append(Particle(center[0], center[1], m=m, r=20, fixed=False, tracker=True))

        return particles

# particles = [
    # Particle(100, 100, v=(1, -1)),
    # # Particle(100, 300),
    # # Particle(300, 300),
    # Particle(220, 220, m=300.0),
# ]

# particles = [
    # Particle(random.randint(100, 900), random.randint(100, 900),
      # v=(random.uniform(-1, 1), random.uniform(-1, 1))) 
        # for _ in range(500)
# ] + [Particle(500, 500, m=100.0, r=4, fixed=False)]

class Sim:

    def __init__(self, particles):
        self.particles = particles

    def update(self):
        t = 0
        # useful = set()
        # fresh = True

        for i1, p1 in enumerate(self.particles):
            if p1.alive:
                for i2 in range(i1 + 1, len(self.particles)):
                    p2 = self.particles[i2]
                    if p2.alive:
                        # if not fresh and (i1, i2) not in self.useful:
                            # continue

                        d = Particle.distance(p1, p2)

                        # if d > 100000.0:
                            # continue
                        # el
                        if d > p1.radius + p2.radius:
                            g_x, g_y = Particle.gravity(p1, p2)

                            p1.add_force(g_x, g_y)
                            p2.add_force(-g_x, -g_y)

                            # if fresh and g_x + g_y > 0.001:
                                # useful.add((i1, i2))
                        else:
                            Particle.collide(p1, p2)

        # fresh = False
        # if t % 10 == 0:
            # print(len(useful))
            # useful = set()
            # fresh = True
        if t % 100 == 0:
            self.particles = [p for p in self.particles if p.alive]
            self.t = 0

        for p in self.particles:
            p.update()

        t += 1

    def add_particles(self, new):
        self.particles += new

class Experiment:

    def __init__(self, n_particles=100, repetitions=1, threshold=1000, d_maxes=[500.0], masses=[100.0]):
        self.n_particles = n_particles
        self.repetitions = repetitions
        self.threshold = threshold
        self.d_maxes = d_maxes
        self.masses = masses

    def run(self):
        print("m | d_max ; i | n left | n in distance | mass in distance")
        for m in self.masses:
            for d in self.d_maxes:
                n_all = 0
                i_all = 0
                n_id_all = 0
                m_id_all = 0
                for _ in range(self.repetitions):
                    sim = Sim(Generator.generate_rotating_disk(n=self.n_particles, d_range=(100, d), m=m))

                    running = True
                    n = len(sim.particles)
                    i = 0
                    i_total = 0
                    while running:
                        sim.update()
     
                        if n == len(sim.particles):
                            i += 1
                        else:
                            n = len(sim.particles)
                            i = 0

                        i_total += 1
                        if i >= self.threshold:
                            running = False
                    n_all += n
                    i_all += i_total
                    n_id, m_id = Experiment.in_distance(sim.particles, d)
                    n_id_all += n_id
                    m_id_all += m_id

                print(m, d, i_all / self.repetitions, n_all / self.repetitions, n_id_all / self.repetitions, m_id_all / self.repetitions)

    def in_distance(particles, distance):
        tracker = particles[0]
        for p in particles:
            if p.tracker:
                tracker = p

        total_mass = 0
        total_mass_in_distance = 0
        n_in_distance = 0
        for p in particles:
            total_mass += p.m
            if p.tracker:
                total_mass_in_distance += p.m
                n_in_distance += 1
                continue

            d = Particle.distance(tracker, p)

            if d < distance:
                total_mass_in_distance += p.m
                n_in_distance += 1
            
        return n_in_distance, total_mass_in_distance / total_mass

class Gui:

    def __init__(self, particles):
        self.sim = Sim(particles)

        self.w, self.h = 600, 600

        pygame.init()
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        self.out = False
        self.turbo = False

        self.x_offset, self.y_offset = -self.w / 2, -self.h / 2
        self.scale = 1

        self.fit()

    def fit(self):
        x_min, x_max = 0, 0
        y_min, y_max = 0, 0

        for p in self.sim.particles:
            if not p.alive:
                continue

            x_min = min(x_min, p.x)
            x_max = max(x_max, p.x)
            y_min = min(y_min, p.y)
            y_max = max(y_max, p.y)

        x_min -= 10
        x_max += 10
        y_min -= 10
        y_max += 10

        self.scale = min(self.w / (x_max - x_min), self.h / (y_max - y_min))

        self.x_offset = x_min
        self.y_offset = y_min

    def center(self):
        p_max = self.sim.particles[0]

        for p in self.sim.particles:
            if not p.alive:
                continue

            if p.m > p_max.m:
                p_max = p

        # self.scale = min(self.w, self.h) / (p_max.radius * 80)

        self.x_offset = p_max.x - (self.w / (2 * self.scale))
        self.y_offset = p_max.y - (self.h / (2 * self.scale))

    def zoom(self, factor):
        x_center = self.x_offset + (self.w / (2 * self.scale))
        y_center = self.y_offset + (self.h / (2 * self.scale))

        self.scale *= factor

        self.x_offset = x_center - (self.w / (2 * self.scale))
        self.y_offset = y_center - (self.h / (2 * self.scale))


    def pan_horizontally(self, factor):
        self.x_offset += factor * self.w / self.scale

    def pan_vertically(self, factor):
        self.y_offset += factor * self.h / self.scale

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.out = True
                    elif event.key == pygame.K_t:
                        self.turbo = not self.turbo
                    elif event.key == pygame.K_a:
                        self.sim.add_particles(Generator.generate_rotating_disk(n=500, d_range=(200, 1000), include_sun=False))
                    elif event.key == pygame.K_f:
                        self.fit()
                    elif event.key == pygame.K_c:
                        self.center()
                    elif event.key == pygame.K_MINUS:
                        self.zoom(0.8)
                    elif event.key == pygame.K_EQUALS:
                        self.zoom(1.25)
                    elif event.key == pygame.K_LEFT:
                        self.pan_horizontally(-0.25)
                    elif event.key == pygame.K_RIGHT:
                        self.pan_horizontally(0.25)
                    elif event.key == pygame.K_UP:
                        self.pan_vertically(-0.25)
                    elif event.key == pygame.K_DOWN:
                        self.pan_vertically(0.25)
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            self.sim.update()
            
            self.screen.fill((0, 0, 0))
            for p in self.sim.particles:
                if self.out:
                    print(p.x, p.y)

                # pygame.draw.rect(screen, (200, 200, 200), (p.x - p.radius, p.y - p.radius, 2 * p.radius, 2 * p.radius))
                pygame.draw.circle(self.screen, p.color, (self.scale * (p.x - self.x_offset), self.scale * (p.y - self.y_offset)), max(self.scale * p.radius, 1))

            self.out = False
            
            # if not turbo_mode or t % 100 == 0:
            pygame.display.flip()
            self.clock.tick(200)

if __name__ == "__main__":
    # Gui(Generator.generate_rotating_disk(n=1000, d_range=(200, 100000))).run()
    Gui(Generator.generate_rotating_disk(n=1000, d_range=(200, 1000))).run()
    # Experiment(threshold=5000.0, repetitions=5, d_maxes=[500, 1000, 5000, 10000], masses=[10.0, 100.0, 500.0, 1000.0, 5000.0, 10000.0]).run()
    # cProfile.run('Sim().run()')

# todo
# center







    
    