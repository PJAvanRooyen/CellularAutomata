import copy

import Cell

import pygame
from pygame import Vector2
from random import randint
import sys

class Boundary(pygame.sprite.Sprite):
    def __init__(self, pointA, pointB, surface, color=None):
        pygame.sprite.Sprite.__init__(self)
        self.a = pointA
        self.b = pointB
        self.surface = surface
        if color is None:
            color = [255, 255, 255]
        pygame.draw.line(self.surface, color, self.a, self.b)

class World:
    def __init__(self, width=1000, height=500):
        pygame.init()

        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode([width, height])
        self.wall_surface = pygame.Surface([width, height], pygame.SRCALPHA)

        self.walls = []
        self.walls.append(Boundary(Vector2(self.width, 0), Vector2(self.width, self.height), self.wall_surface))
        self.walls.append(Boundary(Vector2(0, 0), Vector2(0, self.height), self.wall_surface))
        self.walls.append(Boundary(Vector2(0, 0), Vector2(self.width, 0), self.wall_surface))
        self.walls.append(Boundary(Vector2(0, self.height), Vector2(self.width, self.height), self.wall_surface))

        self.cells = []

    def addWalls(self, wall_count=5):
        for i in range(wall_count):
            x1 = randint(0, self.width)
            y1 = randint(0, self.height)
            x2 = randint(0, self.width)
            y2 = randint(0, self.height)
            self.walls.append(Boundary(Vector2(x1, y1), Vector2(x2, y2), self.wall_surface))

    def addCells(self, cell=Cell.RayParticle(), cell_count=1):
        for i in range(cell_count):
            randomCell = copy.deepcopy(cell)
            randomCell.pos = Vector2((randint(0, self.width), randint(0, self.height)))
            self.cells.append(randomCell)

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    for cell in self.cells:
                        if cell.movement_type == Cell.RayParticle.MovementType.User:
                            cell.move(pos=Vector2(pygame.mouse.get_pos()))
                        else:
                            cell.move()

                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if len(keys) != 0:
                        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                            for cell in self.cells:
                                if cell.movement_type == Cell.RayParticle.MovementType.User:
                                    cell_pos = cell.pos
                                    cell.move(pos=Vector2(cell_pos.x + 1, cell_pos.y))
                                else:
                                    cell.move()
                        if keys[pygame.K_l] or keys[pygame.K_LEFT]:
                            for cell in self.cells:
                                if cell.movement_type == Cell.RayParticle.MovementType.User:
                                    cell_pos = cell.pos
                                    cell.move(pos=Vector2(cell_pos.x - 1, cell_pos.y))
                                else:
                                    cell.move()
                        if keys[pygame.K_w] or keys[pygame.K_UP]:
                            for cell in self.cells:
                                if cell.movement_type == Cell.RayParticle.MovementType.User:
                                    cell_pos = cell.pos
                                    cell.move(pos=Vector2(cell_pos.x, cell_pos.y + 1))
                                else:
                                    cell.move()
                        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                            for cell in self.cells:
                                if cell.movement_type == Cell.RayParticle.MovementType.User:
                                    cell_pos = cell.pos
                                    cell.move(pos=Vector2(cell_pos.x, cell_pos.y - 1))
                                else:
                                    cell.move()

            self.screen.fill([0, 0, 0])
            for i in self.walls:
                self.screen.blit(self.wall_surface, (0, 0))

            for cell in self.cells:
                cell.show(self.screen)
                d = cell.seeWall(self.screen, self.walls, render=True)
                d = cell.seeCell(self.screen, self.cells, render=True)
                # print(d)

            pygame.display.flip()