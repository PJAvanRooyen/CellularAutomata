import Cell
import Environment

def RayTraceExample():
    world = Environment.World()
    world.addWalls(wall_count=2)

    hostCell = Cell.Cell(movement_type=Cell.Cell.MovementType.Auto, ray_cell_detect_count=0)
    world.addCells(cell=hostCell, cell_count=10)

    userCell = Cell.Cell(movement_type=Cell.Cell.MovementType.User, ray_cell_detect_count=2)
    world.addCells(cell=userCell, cell_count=1)

    world.run()

if __name__ == '__main__':
    RayTraceExample()

