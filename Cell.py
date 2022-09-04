import RayTrace

import pygame
from pygame import Vector2
from math import cos, sin, radians
from scipy.spatial import distance
from enum import Enum
from random import randint

class Cell:
    class MovementType(Enum):
        User = 0
        Auto = 1

    def __init__(self, position=Vector2(1, 1), radius=4, angle=0, rayCount=8, ray_cell_detect_count=1, color=[255, 255, 255], movement_type=MovementType.Auto):
        self.pos = position
        self.radius = radius
        self.angle = angle
        self.color = color
        self.movement_type = movement_type
        self.ray_length = 200

        self.rays = []
        self.step = 0
        if rayCount != 0:
            self.step = 360//rayCount
            for i in range(0, 360, self.step):
                self.rays.append(RayTrace.Ray(self.pos, Vector2(cos(radians(i)), sin(radians(i))), self.ray_length))

        self.rays_cell_detect = []
        if ray_cell_detect_count != 0:
            for i in range(0, 360, 360//ray_cell_detect_count):
                self.rays_cell_detect.append(RayTrace.Ray(self.pos, Vector2(cos(radians(i)), sin(radians(i))), self.ray_length))

    def show(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

    def seeWall(self, surface, walls, render):
        distances = []
        for ray in self.rays:
            dmin = 1000000000
            pt = None
            for wall in walls:
                p, d = ray.raycastWall(wall)
                if d is not None and d <= ray.length and d < dmin:
                    dmin = d
                    pt = p

            if pt is not None and render:
                pygame.draw.circle(surface, self.color, [int(pt.x), int(pt.y)], 4)
                pygame.draw.line(surface, self.color, self.pos, pt)
            distances.append(dmin)
        return distances

    def seeCell(self, surface, cells, render):
        distances = []
        seen_cell_positions = []
        for ray in self.rays_cell_detect:
            dmin = 1000000000
            pt = None
            for cell in cells:
                if cell.pos == self.pos or cell.pos in seen_cell_positions:
                    continue

                # cells always detect each other if they are within ray length.
                pos_diff = self.pos - cell.pos
                if abs(pos_diff.x) <= self.ray_length and abs(pos_diff.y) <= self.ray_length:
                    d = distance.euclidean(self.pos, cell.pos)
                    if d is not None and d < dmin:
                        dmin = d
                        pt = cell.pos

            if pt is not None:
                seen_cell_positions.append(pt)
                if render:
                    pygame.draw.circle(surface, self.color, [int(pt.x), int(pt.y)], 4)
                    pygame.draw.line(surface, self.color, self.pos, pt)
            distances.append(dmin)
        return distances

    def randomMove(self, max_pos=Vector2(10000000, 10000000)):
        x = self.pos.x + randint(-3, 3)
        if x < 0:
            x = 0
        elif x > max_pos.x:
            x = max_pos.x

        y = self.pos.y + randint(-3, 3)
        if y < 0:
            y = 0
        elif y > max_pos.y:
            y = max_pos.y

        angle = self.angle + randint(-1, 1)
        if angle < 0:
            angle = 359
        elif angle > 360:
            angle = 1

        self.move(Vector2(x, y), angle)

    def move(self, pos=None, angle=None):
        if pos is None:
            pos = self.pos
        if angle is None:
            angle = self.angle

        self.pos = pos
        for i in self.rays:
            i.pos = self.pos
        self.angle = angle
        if self.step != 0 and len(self.rays) != 0:
            for i in range(0, 360, self.step):
                self.rays[i//self.step].dir = Vector2(cos(radians(i - angle)), sin(radians(i - angle)))
