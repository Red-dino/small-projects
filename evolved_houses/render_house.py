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

def should_place_wall_on_face(house, location, dim):
    x, y, z = location
    x_size, y_size, z_size = dim
    return x < 0 or x > x_size - 1 or y < 0 or y > y_size - 1 or z < 0 or z > z_size - 1 or not house[y][x][z]

def get_3d_polygons_for_house(house):
    polys = []
    counts = [0, 0, 0, 0, 0, 0]

    y_size = len(house)
    x_size = len(house[0])
    z_size = len(house[0][0])
    print(y_size, x_size, z_size)

    for y in range(y_size):
        for x in range(x_size):
            for z in range(z_size):
                block = house[y][x][z]
                if block:
                    if should_place_wall_on_face(house, (x - 1, y, z), dim=(x_size, y_size, z_size)):
                        polys.append([(x, y + 1, z), (x, y, z), (x, y, z + 1), (x, y + 1, z + 1)])
                        counts[0] += 1
                    if should_place_wall_on_face(house, (x + 1, y, z), dim=(x_size, y_size, z_size)):
                        polys.append([(x + 1, y, z + 1), (x + 1, y, z), (x + 1, y + 1, z), (x + 1, y + 1, z + 1)])
                        counts[1] += 1
                    if should_place_wall_on_face(house, (x, y - 1, z), dim=(x_size, y_size, z_size)):
                        polys.append([(x, y, z + 1), (x, y, z), (x + 1, y, z), (x + 1, y, z + 1)])
                        counts[2] += 1
                    if should_place_wall_on_face(house, (x, y + 1, z), dim=(x_size, y_size, z_size)):
                        polys.append([(x + 1, y + 1, z), (x, y + 1, z), (x, y + 1, z + 1), (x + 1, y + 1, z + 1)])
                        counts[3] += 1
                    if should_place_wall_on_face(house, (x, y, z - 1), dim=(x_size, y_size, z_size)):
                        polys.append([(x + 1, y, z), (x, y, z), (x, y + 1, z), (x + 1, y + 1, z)])
                        counts[4] += 1
                    if should_place_wall_on_face(house, (x, y, z + 1), dim=(x_size, y_size, z_size)):
                        polys.append([(x, y + 1, z + 1), (x, y, z + 1), (x + 1, y, z + 1), (x + 1, y + 1, z + 1)])
                        counts[5] += 1
    print(counts)
    return polys
    
def get_xyz_for_sphere_point(radius, theta, phi):
    x0, y0, z0 = 0, 0, radius
    x1 = x0 * math.cos(math.radians(theta)) + y0 * math.sin(math.radians(theta)) * math.sin(math.radians(phi)) + z0 * math.sin(math.radians(theta)) * math.cos(math.radians(phi))
    y1 = y0 * math.cos(math.radians(phi)) - z0 * math.sin(math.radians(phi))
    z1 = -x0 * math.sin(math.radians(theta)) + y0 * math.cos(math.radians(theta)) * math.sin(math.radians(phi)) + z0 * math.cos(math.radians(theta)) * math.cos(math.radians(phi))
    return (x1, y1, z1)

def get_3d_polygons_for_sphere(radius=5, delta=30):
    polys = []
    for t in range(180 // delta):
        for p in range(360 // delta):
            theta = t * delta
            phi = p * delta
            p0 = get_xyz_for_sphere_point(radius, theta + delta, phi)
            p1 = get_xyz_for_sphere_point(radius, theta, phi)
            p2 = get_xyz_for_sphere_point(radius, theta, phi + delta)
            p3 = get_xyz_for_sphere_point(radius, theta + delta, phi + delta)
            if phi > 270 or phi < 90:
                polys.append([p0, p1, p2, p3])
            else:
                polys.append([p2, p1, p0, p3])
    print(len(polys))
    return polys
    
def rot_x(vector, theta):
    x0, y0, z0 = vector
    y1 = y0 * math.cos(math.radians(theta)) - z0 * math.sin(math.radians(theta))
    z1 = y0 * math.sin(math.radians(theta)) + z0 * math.cos(math.radians(theta))
    return x0, y1, z1
    
def get_3d_polygons_for_tire(radius=2, inner_radius=1.5, thickness=1, delta=6):
    polys = []
    thickness = thickness / 2
    for t in range(360 // delta):
        theta = t * delta
        x0, y0, z0 = rot_x((0, 0, radius), theta)
        x1, y1, z1 = rot_x((0, 0, radius), theta + delta)
        x2, y2, z2 = rot_x((0, 0, inner_radius), theta)
        x3, y3, z3 = rot_x((0, 0, inner_radius), theta + delta)
        polys.append([(x0 - thickness, y0, z0), (x0 - thickness, y1, z1), (x0 + thickness, y1, z1), (x0 + thickness, y0, z0)])
        polys.append([(x0 - thickness, y0, z0), (x0 - thickness, y2, z2), (x0 - thickness, y3, z3), (x0 - thickness, y1, z1)])
        polys.append([(x0 + thickness, y0, z0), (x0 + thickness, y1, z1), (x0 + thickness, y3, z3), (x0 + thickness, y2, z2)])
    # print(len(polys))
    return polys
    
def translate_model(model, translation):
    xt, yt, zt = translation
    polys = []
    for poly in model:
        polygon = []
        for point in poly:
            x, y, z = point
            polygon.append((x + xt, y + yt, z + zt))
        polys.append(polygon)
    return polys
    
def get_3d_polygons_for_car():
    polys = []
    ### Left side
    ## Back
    # Back middle panel - base color
    polys.append([(0, 0.75, -0.0625), (0, 0.9375, -0.0625), (0, 0.9375, -1.125), (0, 0.75, -1.21875)])
    # Above light area - base color
    polys.append([(0, 0.9375, -1.125), (0, 0.9375, -1.25), (0, 0.8125, -1.3125), (0, 0.8125, -1.1825)])
    # Back bumper stripe - black
    polys.append([(0, 0.375, -0.921875), (0, 0.5, -0.875), (0, 0.5, -1.5), (0, 0.375, -1.46875)])
    # Back wheel arch
    polys.append([(0, 0.5, -0.0625), (0, 0.75, -0.0625), (0, 0.75, -0.1875), (0, 0.625, -0.1875)])
    polys.append([(0, 0.625, -0.1875), (0, 0.75, -0.1875), (0, 0.75, -0.3125), (0, 0.65625, -0.3125)])
    polys.append([(0, 0.65625, -0.3125), (0, 0.75, -0.3125), (0, 0.75, -0.4375), (0, 0.6875, -0.4375)])
    polys.append([(0, 0.6875, -0.4375), (0, 0.75, -0.4375), (0, 0.75, -0.5625), (0, 0.6875, -0.5625)])
    polys.append([(0, 0.6875, -0.5625), (0, 0.75, -0.5625), (0, 0.75, -0.6875), (0, 0.65625, -0.6875)])
    polys.append([(0, 0.65625, -0.6875), (0, 0.75, -0.6875), (0, 0.75, -0.8125), (0, 0.625, -0.8125)])
    polys.append([(0, 0.625, -0.8125), (0, 0.75, -0.8125), (0, 0.75, -0.875), (0, 0.5, -0.875)])

    ## Middle
    # Bottom middle panel - base color
    polys.append([(0, 0, 0), (0, 0, 2.6875), (0, 0.375, 2.75), (0, 0.375, -0.046875)])
    # Middle stripe - black
    polys.append([(0, 0.375, -0.046875), (0, 0.375, 2.75), (0, 0.5, 2.8125), (0, 0.5, -0.0625)])
    # Front bumper stripe - black
    polys.append([(0, 0.375, 3.71875), (0, 0.375, 4.375), (0, 0.5, 4.375), (0, 0.5, 3.6875)])
    # Top middle panel - base color
    polys.append([(0, 0.5, -0.0625), (0, 0.5, 2.8125), (0, 0.9375, 2.8125), (0, 0.9375, -0.0625)])
    
    ## Front
    # Wheel arch back to front - base color
    polys.append([(0, 0.5, 2.8125), (0, 0.625, 2.9375), (0, 0.75, 2.9375), (0, 0.75, 2.8125)])
    polys.append([(0, 0.625, 2.9375), (0, 0.65625, 3.0625), (0, 0.75, 3.0625), (0, 0.75, 2.9375)])
    polys.append([(0, 0.65625, 3.0625), (0, 0.6875, 3.1875), (0, 0.75, 3.1875), (0, 0.75, 3.0625)])
    polys.append([(0, 0.6875, 3.1875), (0, 0.6875, 3.3125), (0, 0.75, 3.3125), (0, 0.75, 3.1875)])
    polys.append([(0, 0.6875, 3.3125), (0, 0.65625, 3.4375), (0, 0.75, 3.4375), (0, 0.75, 3.3125)])
    polys.append([(0, 0.65625, 3.4375), (0, 0.625, 3.5625), (0, 0.75, 3.5625), (0, 0.75, 3.4375)])
    polys.append([(0, 0.625, 3.5625), (0, 0.5, 3.6875), (0, 0.75, 3.6875), (0, 0.75, 3.5625)])
    # Top front panel - base color
    polys.append([(0, 0.9375, 2.8125), (0, 0.75, 2.8125), (0, 0.75, 4)])
    # Middle front panel - base color
    polys.append([(0, 0.5625, 3.6875), (0, 0.5625, 3.9375), (0, 0.75, 4), (0, 0.75, 3.6875)])
    # Headlight side - Headlight color
    polys.append([(0, 0.75, 4), (0, 0.5625, 3.9375), (0, 0.5625, 4.1875), (0, 0.75, 4.15625)])
    # Top front bumper - base color/bumper color
    polys.append([(0, 0.5, 3.6875), (0, 0.5, 4.375), (0, 0.5625, 4.34375), (0, 0.5625, 3.6875)])
    
    ## Door and above
    # Front window - window color
    polys.append([(0, 0.9375, 0.6250), (0, 0.9375, 2.5625), (0.2045, 1.5625, 1.6250), (0.2045, 1.5625, 0.5625)])
    # Window divider - black
    polys.append([(0, 0.9375, 0.6250), (0.2045, 1.5625, 0.5625), (0.2045, 1.5625, 0.425), (0, 0.9375, 0.4375)])
    # Back window - window color
    polys.append([(0, 0.9375, 0.4375), (0.2045, 1.5625, 0.425), (0.2045, 1.53125, -0.1375), (0, 1, -0.90625)])
    # Back window aligner - base color
    polys.append([(0, 0.9375, 0.4375), (0, 1.02, -1.21875), (0, 0.9375, -1.25)])
    # Front window top sill - base color
    polys.append([(0.2045, 1.5625, 1.625), (0.25, 1.625, 1.6250), (0.25, 1.625, 0.425), (0.2045, 1.5625, 0.425)])
    
    ## Wheels
    polys.extend(translate_model(get_3d_polygons_for_tire(radius=0.4375, inner_radius=0.25, thickness=0.3125, delta=15), (0.15625, 0.0625, 3.25)))
    polys.extend(translate_model(get_3d_polygons_for_tire(radius=0.4375, inner_radius=0.25, thickness=0.3125, delta=15), (0.15625, 0.0625, -0.5)))
    
    ### Roof
    # Roof front panel - base color
    polys.append([(0.25, 1.625, 0.425), (0.25, 1.625, 1.6250), (1.890, 1.625, 1.6250), (1.890, 1.625, 0.425)])
    # Roof back panel - base color
    polys.append([(0.25, 1.625, 0.425), (1.890, 1.625, 0.425), (1.890, 1.6, -0.2), (0.25, 1.6, -0.2)])
    
    ### Hood
    # Left top panel - base color
    polys.append([(0, 0.9375, 2.8125), (0, 0.75, 4.15625), (0.5, 0.75, 4.15625), (0.3125, 0.9375, 2.8125)])
    # Right top panel - base color
    polys.append([(2.25, 0.9375, 2.8125), (2.25, 0.75, 4.15625), (1.75, 0.75, 4.15625), (1.9375, 0.9375, 2.8125)])
    # Center panel - base color
    polys.append([(0.3125, 0.875, 2.8125), (0.5, 0.6875, 4.15625), (1.75, 0.6875, 4.15625), (1.9375, 0.875, 2.8125)])
    # Left center panel joiner - base color
    polys.append([(0.3125, 0.875, 2.8125), (0.5, 0.6875, 4.15625), (0.5, 0.75, 4.15625), (0.3125, 0.9375, 2.8125)])
    # Right center panel joiner - base color
    polys.append([(1.9375, 0.875, 2.8125), (1.75, 0.6875, 4.15625), (1.75, 0.75, 4.15625), (1.9375, 0.9375, 2.8125)])
    # Front middle panel - base color
    polys.append([(1.75, 0.6875, 4.15625), (0.5, 0.6875, 4.15625), (0.5, 0.5625, 4.1875), (1.75, 0.5625, 4.1875)])
    # Front accent strip
    # Bumper top - bumper color
    polys.append([(0, 0.5625, 4.1875), (0, 0.5625, 4.34375), (2.25, 0.5625, 4.34375), (2.25, 0.5625, 4.1875)])
    

    print(len(polys))
    return polys

def normalize(vector):
    x, y, z = vector
    factor = 1.0 / math.sqrt((x ** 2) + (y ** 2) + (z ** 2))
    return (x * factor, y * factor, z * factor)
 
def rot_y(vector, theta):
    sin_theta = math.sin(math.radians(theta))
    cos_theta = math.cos(math.radians(theta))
    
    x, y, z = vector
    
    x_rot = x * cos_theta + z * sin_theta
    z_rot = -x * sin_theta + z * cos_theta
    return x_rot, y, z_rot

def get_normal_for_square_poly(poly, theta):
    p0x, p0y, p0z = poly[0]
    p1x, p1y, p1z = poly[1]
    p2x, p2y, p2z = poly[2]
    
    p0y, p1y, p2y = -p0y, -p1y, -p2y
    
    v0x, v0y, v0z = p0x - p1x, p0y - p1y, p0z - p1z
    v1x, v1y, v1z = p2x - p1x, p2y - p1y, p2z - p1z
    
    norm_x = v0y * v1z - v0z * v1y
    norm_y = v0z * v1x - v0x * v1z
    norm_z = v0x * v1y - v0y * v1x
    
    return rot_y(normalize((norm_x, norm_y, norm_z)), theta)
    
def get_brightness_for_poly(poly, light_loc=(0, 0, 0)):
    n_x, n_y, n_z = get_normal_for_square_poly(poly, 0)
    p1x, p1y, p1z = poly[0]
    p1y = -p1y
    
    p1x -= light_loc[0]
    p1y -= light_loc[1]
    p1z -= light_loc[2]
    
    p2x, p2y, p2z = normalize((p1x, p1y, p1z))
    return (p2x * n_x + p2y * n_y + p2z * n_z + 1) / 2

def get_projected_polygons(polys, camera_loc=(0, 0, 0), theta=None, phi=None, width=480, include_brightness=False):
    polys2d = []
    brightnesses = []
    z_values = []

    for poly in polys:
        # Norm calc
        n_x, n_y, n_z = get_normal_for_square_poly(poly, theta)

        poly2d = []
        z_in_poly = []
        for point in poly:
            x, y, z = point
            x, y, z = x, -y, z
            
            # Camera transform
            x -= camera_loc[0]
            y -= camera_loc[1]
            z -= camera_loc[2]
            
            if theta != None:
                x, y, z = rot_y((x, y, z), theta)
            
            # Normal dot
            if z <= 0: # or n_x * x + n_y * y + n_z * z > 0:
                # print("loc", point)
                # print("rel", x, y, z)
                # print("normal", n_x, n_y, n_z)
                continue

            # Project
            scale = width / (2 * z)

            poly2d.append((scale * x + 240, scale * y + 180))
            z_in_poly.append(z)
        if len(poly2d) > 2:
            polys2d.append(poly2d)
            if include_brightness:
                z_avg = 0
                for z in z_in_poly:
                    z_avg += z
                z_values.append(z_avg / len(z_in_poly))
                brightnesses.append(get_brightness_for_poly(poly, light_loc=(10, 10, 4)))

    if include_brightness:
        if len(polys2d) == 0:
            return [], []
    
        start = time.time()
        _, polys2d, brightnesses = zip(*sorted(zip(z_values, polys2d, brightnesses), key=lambda val: val[0], reverse=True))
        # print("sort", time.time() - start)
        return polys2d, brightnesses
    else:
        return polys2d
        
def redraw(screen, polys, camera_loc, theta):
    screen.fill((150, 150, 255))
    # calc_start = time.time()
    polys2d, brightnesses = get_projected_polygons(polys, camera_loc=camera_loc, theta=theta, include_brightness=True)
    start = time.time()
    # print("calc", start - calc_start)
    for i in range(len(polys2d)):
        poly = polys2d[i]
        light = brightnesses[i]
        # pygame.draw.polygon(screen, (147 * light, 145 * light, 122 * light), poly, 0)
        pygame.draw.polygon(screen, (255 * light, 0, 0), poly, 0)
        # pygame.draw.aalines(screen, (147 * light, 145 * light, 122 * light), True, poly, 1)
    draw_crosshairs(screen)
    # print("draw", time.time() - start)

def draw_crosshairs(screen):
    pygame.draw.line(screen, (0, 0, 0, 255), (235, 180), (245, 180), 1)
    pygame.draw.line(screen, (0, 0, 0, 255), (240, 175), (240, 185), 1)

def draw_fps(screen, font, fps):
    text_surf = font.render(str(fps), (0, 0, 0), (255, 255, 255))[0]
    screen.blit(text_surf, (1, 1))

def render_poly3d(polys):
    pygame.init()
    pygame.display.set_caption("House")
    screen = pygame.display.set_mode((480, 360), FULLSCREEN)

    clock = pygame.time.Clock()
    
    font = pygame.freetype.SysFont("Consolas", 12)

    c_x, c_y, c_z = -5, -3, -20
    theta = 0

    redraw(screen, polys, (c_x, c_y, c_z), theta)

    # Smooth moving
    move_speed = 0.5
    move_forward = False
    move_back = False
    move_left = False
    move_right = False

    focused = False
    update = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    c_y -= 1
                    update = True
                elif event.key == K_DOWN:
                    c_y += 1
                    update = True
                elif event.key == K_a:
                    move_left = True
                elif event.key == K_d:
                    move_right = True
                elif event.key == K_w:
                    move_forward = True
                elif event.key == K_s:
                    move_back = True
                elif event.key == K_LEFT:
                    theta += 15
                    update = True
                elif event.key == K_RIGHT:
                    theta -= 15
                    update = True
                elif event.key == K_ESCAPE:
                    focused = False
                    running = False
                # print(clock.get_fps())
                # redraw(screen, polys, (c_x, c_y, c_z), theta)
            elif event.type == KEYUP:
                if event.key == K_a:
                    move_left = False
                elif event.key == K_d:
                    move_right = False
                elif event.key == K_w:
                    move_forward = False
                elif event.key == K_s:
                    move_back = False
            elif event.type == MOUSEBUTTONDOWN:
                focused = True
                pygame.mouse.set_visible(False)
        
        if move_forward:
            c_x -= move_speed * math.sin(math.radians(theta))
            c_z += move_speed * math.cos(math.radians(theta))
            update = True
        elif move_back:
            c_x += move_speed * math.sin(math.radians(theta))
            c_z -= move_speed * math.cos(math.radians(theta))
            update = True
        if move_left:
            c_z -= move_speed * math.sin(math.radians(theta))
            c_x -= move_speed * math.cos(math.radians(theta))
            update = True
        elif move_right:
            c_z += move_speed * math.sin(math.radians(theta))
            c_x += move_speed * math.cos(math.radians(theta))
            update = True

        if focused:
            mouse_x, _ = pygame.mouse.get_pos()
            pygame.mouse.set_pos((240, 180))
            delta_theta = 0.2 * (mouse_x - 240)
            if delta_theta != 0:
                theta -= delta_theta
                update = True

        if update:
            redraw(screen, polys, (c_x, c_y, c_z), theta)
            draw_fps(screen, font, clock.get_fps())
            update = False

        pygame.display.flip()
        clock.tick(60)
