import Cell
import Environment
from pygame import Vector2

if __name__ == '__main__':
    world = Environment.World()
    # world.addWalls(5)

    hostCell = Cell.RayParticle(movement_type=Cell.RayParticle.MovementType.Auto, ray_cell_detect_count=0)
    world.addCells(cell=hostCell, cell_count=10)

    userCell = Cell.RayParticle(movement_type=Cell.RayParticle.MovementType.User, ray_cell_detect_count=2)
    world.addCells(userCell, 1)

    world.run()

