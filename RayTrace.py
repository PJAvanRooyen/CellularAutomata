import pygame
from pygame import Vector2

class Ray:
    def __init__(self, position, direction, length):
        self.pos = position
        self.dir = direction
        self.length = length
        self.intersection = None

    def point(self, newDir):
        self.dir = newDir - self.pos
        self.dir.scale_to_length(20)

    def show(self, surface, color=None):
        if color is None:
            color = [255, 255, 255]
        pygame.draw.line(surface, color, self.pos, self.pos + self.length * self.dir)

    def raycastWall(self, wall):
        # TODO: check distances before for efficiency

        x1 = wall.a.x
        y1 = wall.a.y
        x2 = wall.b.x
        y2 = wall.b.y

        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if den == 0:
            return None, None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if 0 < t < 1 and u > 0:
            self.intersection = Vector2()
            self.intersection.x = float(x1 + t * (x2 - x1))
            self.intersection.y = float(y1 + t * (y2 - y1))
            return self.intersection, u
        else:
            return None, None