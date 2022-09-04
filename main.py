import Cell
import Environment
from pygame import Vector2

if __name__ == '__main__':
    world = Environment.World()
    # world.addWalls(5)
    world.addCells(cell_count=2)

    userCell = Cell.RayParticle(Vector2(250, 250), movement_type=Cell.RayParticle.MovementType.User)
    world.addCells(userCell, 1)

    world.run()

