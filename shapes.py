from __future__ import annotations

import pygame
import math


def fade_color(start: pygame.Color, end: pygame.Color, factor: float):
    factor = 0 if factor < 0 else 1 if factor > 1 else factor
    blend = pygame.Color(0, 0, 0)
    blend.r = int(round(start.r + (end.r - start.r) * factor))
    blend.g = int(round(start.g + (end.g - start.g) * factor))
    blend.b = int(round(start.b + (end.b - start.b) * factor))
    return blend


class Shape:
    def draw(self, surface: pygame.Surface, color: pygame.Color):
        if isinstance(self, Point):
            pygame.draw.circle(surface, color, (self.x, self.y), 0)

        if isinstance(self, Rect):
            pygame.draw.rect(surface, color, (self.x, self.y, self.w, self.h))

        if isinstance(self, Circ):
            pygame.draw.circle(surface, color, (self.x, self.y), self.r)

        if isinstance(self, Line):
            pygame.draw.line(surface, color, (self.x1, self.y1), (self.x2, self.y2))

        if isinstance(self, Polygon):
            pygame.draw.polygon(surface, color, (self.points))

        if isinstance(self, Text):
            font = pygame.font.SysFont(
                self.options.get("font"), self.options.get("size")
            )
            message = font.render(self.text, True, color)

            position = (self.x, self.y)
            if self.options.get("center"):
                position = message.get_rect(center=(self.x, self.y))

            surface.blit(message, position)

    def collide(self, other: Shape):
        if isinstance(self, Point) and isinstance(other, Point):
            return self.x == other.x and self.y == other.y

        if isinstance(self, Rect) and isinstance(other, Rect):
            r1 = pygame.Rect(self.x, self.y, self.w, self.h)
            r2 = pygame.Rect(other.x, other.y, other.w, other.h)
            return r1.colliderect(r2)

        if isinstance(self, Circ) and isinstance(other, Circ):
            dist = math.hypot(self.x - other.x, self.y - other.y)
            return dist <= self.r + other.r

        return False


class Point(Shape):
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rect(Shape):
    def __init__(self, x, y, w=1, h=1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Circ(Shape):
    def __init__(self, x, y, r=1):
        self.x = x
        self.y = y
        self.r = r


class Line(Shape):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Polygon(Shape):
    def __init__(self, points):
        self.points = points


class Text(Shape):
    def __init__(self, x, y, text="", *, center=False, font=None, size=16):
        self.x = x
        self.y = y
        self.text = text
        self.options = {"center": center, "font": font, "size": size}
