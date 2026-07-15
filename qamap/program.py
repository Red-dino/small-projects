import pygame, sys
import pygame.freetype
from pygame.locals import *
from enum import Enum, auto
import random
import math

pygame.init()

pygame.display.set_caption("qamap")

screen_size = (1200, 800)

screen = pygame.display.set_mode(screen_size, pygame.RESIZABLE)

pygame.display.set_icon(pygame.image.load("icon.png"))

font = pygame.freetype.Font("Kalam-Regular.ttf", 12)

running = True
clock = pygame.time.Clock()

class BoxActionType(Enum):
    NONE = auto()
    DRAG = auto()
    INPUT = auto()
    CONNECT = auto()
    DELETE = auto()
    HOVER = auto()
    HOVER_DROP = auto()

    # TOP = PARENT, BOTTOM = CHILD
    START_TOP = auto()
    START_BOTTOM = auto()
    END_TOP = auto()
    END_BOTTOM = auto()

    # A specific
    TOGGLE_COMPLETE = auto()

class BoxType(Enum):
    Q = auto()
    A = auto()

class Box:

    curr_box_id = 0

    VALID_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890 .,!?/\\;:'\"[{]}()~@#$%^&|`=+-_\r"
    
    def __init__(self, pos, dim, box_type=BoxType.Q):
        self.id = Box.curr_box_id
        Box.curr_box_id += 1
        self.box_type = box_type
        self.dim = dim
        self._update_pos(pos)
        self.text_size = 28

        self.shadow_color = (60, 40, 40) if self.box_type == BoxType.Q else (40, 40, 60)
        self.bg_color = (200, 100, 100) if self.box_type == BoxType.Q else (100, 100, 200)
        self.hover_color = (180, 80, 80) if self.box_type == BoxType.Q else (80, 80, 180)

        self.text = "How many?"
        self.text_lines = ["How many?"]

        self.being_dragged = False
        self.rel_drag_pos = (0, 0)

        self.is_top_hovered = False
        self.is_center_hovered = False
        self.is_bottom_hovered = False

        self.curr_unicode = None
        self.type_start_time = pygame.time.get_ticks()

        self.complete = False

    def _update_pos(self, new_pos):
        self.pos = new_pos
        self.rect = pygame.Rect(self.pos, self.dim)
        self.top_rect = pygame.Rect(self.pos, (self.dim[0], 28))
        self.center_rect = pygame.Rect(self.top_rect.bottomleft, (self.dim[0], self.dim[1] - 56))
        self.bottom_rect = pygame.Rect((self.pos[0], self.pos[1] + self.dim[1] - 28), (self.dim[0], 28))

    def _toggle_complete(self):
        self.complete = not self.complete
        self.shadow_color = (40, 60, 40) if self.complete else (40, 40, 60)
        self.bg_color = (100, 200, 100) if self.complete else (100, 100, 200)
        self.hover_color = (80, 180, 80) if self.complete else (80, 80, 180)

    def get_top_anchor_pos(self):
        x, y = self.pos
        w, h = self.dim
        return (x + w / 2 - 4, y + 10)

    def get_bottom_anchor_pos(self):
        x, y = self.pos
        w, h = self.dim
        return (x + w / 2 - 4, y + h - 18)

    def _calc_space_suffix_len(self, string):
        n = 0
        for i in range(len(string)):
            if string[-i] != " ":
                return n
            n += 1
        return n

    def draw(self, screen):
        x, y = self.pos
        w, h = self.dim
        # shadow
        pygame.draw.rect(screen, self.shadow_color, (x - 3, y - 3, w, h))

        # bg
        pygame.draw.rect(screen, self.bg_color, (x, y, w, h))
        if self.is_center_hovered:
            pygame.draw.rect(screen, self.hover_color, self.center_rect)

        line_y = 0
        t_w, t_h = (0, 0)
        space_mod = 0
        for line in self.text_lines:
            text_surf = font.render(line, (10, 10, 10), size=self.text_size)[0]
            t_w, t_h = text_surf.get_size()
            space_mod = self._calc_space_suffix_len(line) * 10
            screen.blit(text_surf, (x + 8, y + 38 + line_y))
            line_y += self.text_size
        if self.is_center_hovered:
            line_y -= self.text_size
            pygame.draw.line(screen, (10, 10, 10), (x + 10 + t_w + space_mod, y + line_y + 36), (x + 10 + t_w + space_mod, y + line_y + t_h + 40))
        
        # top anchor
        if self.is_top_hovered:
            pygame.draw.rect(screen, self.hover_color, self.top_rect)
        pygame.draw.rect(screen, self.shadow_color, (x + w / 2 - 4, y + 10, 8, 8))

        # bottom anchor
        if self.is_bottom_hovered:
            pygame.draw.rect(screen, self.hover_color, self.bottom_rect)
        if self.box_type == BoxType.Q:
            pygame.draw.rect(screen, self.shadow_color, (x + w / 2 - 4, y + h - 18, 8, 8))
        else:
            pygame.draw.rect(screen, self.shadow_color, (x + w / 2 - 4, y + h - 18, 8, 8), 0 if self.complete else 2)

        # border
        pygame.draw.rect(screen, self.shadow_color, (x, y, w, h), 1)

        if self.curr_unicode and pygame.time.get_ticks() - self.type_start_time > 500:
            self._add_char(self.curr_unicode)

    def _wrap_text(self):
        self.text_lines = []

        curr_line = ""
        for line in self.text.split("\r"):
            for word in line.split(" "):
                string = curr_line + " " + word if curr_line != "" else word
                _, _, line_w, line_h = font.get_rect(string, size=self.text_size)
                if line_w <= self.dim[0] - 16:
                    curr_line = string
                else:
                    self.text_lines.append(curr_line)
                    curr_line = word
            self.text_lines.append(curr_line)
            curr_line = ""

    def _add_char(self, char):
        if char == "\b":
            self.text = self.text[0:max(0, len(self.text) - 1)]
            self._wrap_text()
        if char in Box.VALID_CHARS:
            self.text += char
            self._wrap_text()

    def handle_event(self, event, mouse_pos):
        m_x, m_y = mouse_pos

        self.is_top_hovered = self.top_rect.collidepoint(mouse_pos) and not self.being_dragged
        self.is_center_hovered = self.center_rect.collidepoint(mouse_pos)
        self.is_bottom_hovered = self.bottom_rect.collidepoint(mouse_pos) and not self.being_dragged

        if (not self.rect.collidepoint(mouse_pos)) and not self.being_dragged:
            self.curr_unicode = None
            return BoxActionType.NONE

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.is_top_hovered:
                    return BoxActionType.START_TOP
                elif self.is_bottom_hovered:
                    if self.box_type == BoxType.Q:
                        return BoxActionType.START_BOTTOM
                    elif self.box_type == BoxType.A:
                        self._toggle_complete()
                        return BoxActionType.TOGGLE_COMPLETE
                else:
                    self.being_dragged = True
                    self.rel_drag_pos = (self.pos[0] - m_x, self.pos[1] - m_y)
                    return BoxActionType.DRAG
            elif event.button == 3:
                return BoxActionType.DELETE
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_top_hovered:
                    return BoxActionType.END_TOP
                elif self.is_bottom_hovered:
                    return BoxActionType.END_BOTTOM if self.box_type != BoxType.A else BoxActionType.HOVER_DROP
                elif self.being_dragged:
                    self.being_dragged = False
                    return BoxActionType.DRAG
                else:
                    return BoxActionType.HOVER_DROP
        elif event.type == pygame.MOUSEMOTION:
            if self.being_dragged:
                self._update_pos((m_x + self.rel_drag_pos[0], m_y + self.rel_drag_pos[1]))
                return BoxActionType.DRAG

        if event.type == pygame.KEYDOWN:
            self.curr_unicode = event.unicode
            self.type_start_time = pygame.time.get_ticks()
            self._add_char(self.curr_unicode)
            return BoxActionType.INPUT
        elif event.type == pygame.KEYUP:
            self.curr_unicode = None
            return BoxActionType.INPUT
            

        return BoxActionType.HOVER

class Connection:

    def __init__(self):
        self.top_box = None
        self.bottom_box = None

    def draw(self, screen):
        x1, y1 = self.top_box.get_top_anchor_pos()
        x2, y2 = self.bottom_box.get_bottom_anchor_pos()
        pygame.draw.line(screen, (60, 40, 40), (x1 + 3, y1 + 3), (x2 + 3, y2 + 3), 4)

    def draw_with_drag_pos(self, screen, mouse_pos):
        if self.top_box:
            x, y = self.top_box.get_top_anchor_pos()
            pygame.draw.line(screen, (60, 40, 40), (x + 3, y + 3), mouse_pos, 4)
        elif self.bottom_box:
            x, y = self.bottom_box.get_bottom_anchor_pos()
            pygame.draw.line(screen, (60, 40, 40), mouse_pos, (x + 3, y + 3), 4)

default_box_dim = (220, 266)

boxes = [Box((10, 10), default_box_dim, box_type=BoxType.A)]
connections = dict()

curr_connection = None

corner = pygame.Rect(0, 0, 50, 50)

while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == VIDEORESIZE:
            screen_size = event.size
            screen = pygame.display.set_mode(event.size, RESIZABLE)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and corner.collidepoint(mouse_pos):
                box = Box(mouse_pos, default_box_dim, box_type=BoxType.A)
                box.being_dragged = True
                boxes.append(box)
                continue

            used = False
            for box in reversed(boxes):
                action_type = box.handle_event(event, mouse_pos)
                if action_type != BoxActionType.NONE:
                    boxes.remove(box)
                    if action_type != BoxActionType.DELETE:
                        boxes.append(box)
                    else:
                        keys_to_delete = []
                        for key in connections.keys():
                            if box.id in key:
                                keys_to_delete.append(key)
                        for k in keys_to_delete:
                            del connections[k]
                    used = True

                    # Handle connection
                    if action_type == BoxActionType.START_TOP:
                        curr_connection = Connection()
                        curr_connection.top_box = box
                    elif action_type == BoxActionType.START_BOTTOM:
                        curr_connection = Connection()
                        curr_connection.bottom_box = box
                    elif action_type == BoxActionType.END_TOP:
                        if curr_connection and curr_connection.bottom_box:
                            curr_connection.top_box = box
                            key = (curr_connection.top_box.id, curr_connection.bottom_box.id)

                            if key[0] == key[1]:
                                pass
                            elif key in connections:
                                del connections[key]
                            else:
                                connections[key] = curr_connection
                        curr_connection = None
                    elif action_type == BoxActionType.END_BOTTOM:
                        if curr_connection and curr_connection.top_box:
                            curr_connection.bottom_box = box
                            key = (curr_connection.top_box.id, curr_connection.bottom_box.id)

                            if key[0] == key[1]:
                                pass
                            elif key in connections:
                                del connections[key]
                            else:
                                connections[key] = curr_connection
                        curr_connection = None
                    elif action_type == BoxActionType.HOVER_DROP:
                        curr_connection = None

                    break
            if not used:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    boxes.append(Box(mouse_pos, default_box_dim))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    curr_connection = None

    screen.fill((220, 220, 220))

    for x in range(20, screen_size[0], 40):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, screen_size[1]))
    for y in range(20, screen_size[1], 40):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (screen_size[0], y))
            

    for box in boxes:
        box.draw(screen)

    for connection in connections.values():
        connection.draw(screen)

    if curr_connection:
        curr_connection.draw_with_drag_pos(screen, mouse_pos)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()