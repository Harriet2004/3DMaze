# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Wall following maze solver.
#
# _author_ = 'Jeffrey Chan'
# _copyright_ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

class WallFollowingMazeSolver(MazeSolver):
    """
    Wall following solver implementation without using a Directions enum.
    """

    def __init__(self):
        super().__init__()
        self.m_name = "wall"
        # Define direction vectors
        self.directions = {
            'NORTH': Coordinates3D(0, 1, 0),
            'NORTH_EAST': Coordinates3D(1, 0, 0),
            'EAST': Coordinates3D(0, 0, 1),
            'SOUTH': Coordinates3D(0, -1, 0),
            'SOUTH_WEST': Coordinates3D(-1, 0, 0),
            'WEST': Coordinates3D(0, 0, -1),
        }
        self.direction_order = ['NORTH', 'NORTH_EAST', 'EAST' , 'SOUTH', 'SOUTH_WEST', 'WEST']

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solved = False
        startCoord: Coordinates3D = entrance
        currCell: Coordinates3D = startCoord
        currDirection = 'NORTH'

        while currCell not in maze.getExits():
            # append cell visited 
            self.solverPathAppend(currCell)

            # Get list of neighbours
            neighbours : list[Coordinates3D] = maze.neighbours(currCell)

            # Neighbours that can be visited (non-walls)
            possibleNeighs: list[Coordinates3D] = [ neigh for neigh in neighbours if not maze.hasWall(currCell, neigh) and \
                                                   (neigh.getRow() >= 0) and (neigh.getRow() <= maze.rowNum(neigh.getLevel())) \
                                                    and (neigh.getCol() >= 0) and (neigh.getCol() <= maze.colNum(neigh.getLevel())) ]


            # # Get opposite direction (which cell you came from)
            current_index = self.direction_order.index(currDirection)
            next_index = (current_index + 3) % len(self.direction_order)
            currDirection = self.direction_order[next_index]

            # Check wall one rotation to the left
            current_index = self.direction_order.index(currDirection)
            next_index = (current_index - 1) % len(self.direction_order)
            currDirection = self.direction_order[next_index]
            # While cannot move forward
            while (currCell + self.directions[currDirection]) not in possibleNeighs:
                # Check wall one rotation to the left
                current_index = self.direction_order.index(currDirection)
                next_index = (current_index - 1) % len(self.direction_order)
                currDirection = self.direction_order[next_index]

            # Move forward if there is no wall
            currCell = currCell + self.directions[currDirection]

        # ensure we are currently at the exit
        if currCell in maze.getExits():
            # append exit cell to solverPath
            self.solverPathAppend(currCell)
            self.solved(entrance, currCell)