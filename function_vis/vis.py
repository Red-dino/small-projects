import pygame
import pygame.freetype
import math
import time

from pygame.locals import (
    K_ESCAPE,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_s,
    K_a,
    K_d,
    KEYDOWN,
    KEYUP,
    QUIT,
    MOUSEBUTTONDOWN,
    FULLSCREEN
)

W = 90
H = 90
SCALE = 4

def color(x, y, t):
    return squash(abs(200 * math.sin(x / 4)) * (math.exp(x - (y * t / 30)) / (t / 20)), abs(200 * math.cos(y / 4)), abs(255 * math.sin(t / 360)))

def wiggle(x, y, t):
    dist = math.sqrt((x - 45) ** 2 + (y - 45) ** 2) * t
    return squash(dist, t, dist)

def wiggle_y(x, y, t):
    dist = math.sqrt((x - 45) ** 2 + (y - 45 + t) ** 2) * t
    return squash(dist, dist, dist)

def squashed_circle(x, y, t):
    dist = math.sqrt((x - 45) ** 2 + (y - 45) ** 2) * 200
    return squash(dist, dist, dist)

def noise_codex(x, y, t):
    return flat_squash((y + t) ** x)

def endless(x, y, t):
    return flat_squash(t * y * x)
    
def endless_centered(x, y, t):
    x = x - (W / 2)
    y = y - (H / 2)
    return flat_squash(t * y * x * 1)
    
def diag_scanlines(x, y, t):
    x = x - (W / 2)
    y = y - (H / 2)
    return flat_squash(t + y + x)

def adam_and_god(x, y, t):
    x = x - (W / 2)
    y = y - (H / 2)
    return flat_squash(math.exp(x * y / 3) - math.sqrt(t))

def ribs(x, y, t):
    return flat_squash(math.sqrt(x * y / t) * t)

def endless_bouncy(x, y, t):
    return flat_squash(t * math.sin(t / 90) * x * y)
    
def diag_echos(x, y, t):
    return flat_squash(t * math.sin(t / (x + y + 1)) * x * y)
    
def meteor(x, y, t):
    return flat_squash(t * math.sin(t / (x * y + 1)) * x * y)

def exp_beam(x, y, t):
    return flat_squash(math.exp(x + y * math.cos(t / 90)))
    
def diag_squares(x, y, t):
    return bw_squash(math.sqrt(x + y + t))
    
def hyper_beam(x, y, t):
    return bw_squash(math.sqrt(t * x * y))
    
def q(x, y, t):
    return bw_squash(math.sqrt(t + x * y))

def squash(r, g, b):
    return (r % 255, g % 255, b % 255)
    
def flat_squash(n):
    flat_n = n % 16777216
    return (flat_n // 65536, flat_n // 256 % 256, flat_n % 256)

def bw_squash(n):
    c = (int(n) % 2) * 255
    return (c, c, c)

def draw_loop():
    pygame.init()
    pygame.display.set_caption("Vis")
    screen = pygame.display.set_mode((W * SCALE, H * SCALE))
    
    surf = pygame.Surface((W, H))

    clock = pygame.time.Clock()

    frame = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        # pixels = pygame.PixelArray(screen)
        for x in range(W):
            for y in range(H):
                surf.set_at((x, y), hyper_beam(x, y, frame))
                # pixels[x][y] = color(x, y, frame)
        # pixels.close()

        screen.blit(pygame.transform.scale(surf, (W * SCALE, H * SCALE)), (0, 0))

        pygame.display.flip()
        clock.tick(60)
        
        frame += 1
        
if __name__ == "__main__":
    draw_loop()

