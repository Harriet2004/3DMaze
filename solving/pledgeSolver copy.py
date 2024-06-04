# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Pledge maze solver.
#
# _author_ = 'Jeffrey Chan'
# _copyright_ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D

from random import choice

class PledgeMazeSolver(MazeSolver):
    """
    Pledge solver implementation.  You'll need to complete its implementation for task B.
    """

    def _init_(self):
        super()._init_()
        self.m_name = "pledge"
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
        # TODO: Implement this for task B!
        self.m_solved = False

        # select starting cell
        startCoord: Coordinates3D = entrance

        currCell: Coordinates3D = startCoord

        # Select a direction of preference
        selectDirection = choice(self.direction_order)

        while currCell not in maze.getExits():
            # find all neighbours of current cell
            neighbours: list[Coordinates3D] = maze.neighbours(currCell)

            # filter to ones that haven't been visited and within boundary and doesn't have a wall between them
            possibleNeighs: list[Coordinates3D] = [
                neigh
                for neigh in neighbours
                if not maze.hasWall(currCell, neigh)
                and (neigh.getRow() >= -1)
                and (neigh.getRow() <= maze.rowNum(neigh.getLevel()))
                and (neigh.getCol() >= -1)
                and (neigh.getCol() <= maze.colNum(neigh.getLevel()))
            ]

            # Travel in selectDirection until hitting a wall
            # If there is not a wall in selectDirection
            if currCell + self.directions[selectDirection] in possibleNeighs:
                # Move in that direction
                currCell = currCell + self.directions[selectDirection]
            # Else there is a wall, perform wall following
            else:
                # Perform wall following
                # Start counter at 0; negative is a left turn, and positive is a right turn
                counter: int = 0
                # currDirection is selectDirection
                currDirection = selectDirection
                # turn left instead of right for right-wall follower
                # Get opposite direction (which cell you came from)
                current_index = self.direction_order.index(currDirection)
                next_index = (current_index + 3) % len(self.direction_order)
                currDirection = self.direction_order[next_index]

                # Check wall one rotation to the left
                current_index = self.direction_order.index(currDirection)
                next_index = (current_index - 1) % len(self.direction_order)
                currDirection = self.direction_order[next_index]

                # While cannot move forward
                while (currCell + self.directions[currDirection]) not in possibleNeighs:
                    # Check wall one rotation to the left, save to counter
                    current_index = self.direction_order.index(currDirection)
                    next_index = (current_index - 1) % len(self.direction_order)
                    currDirection = self.direction_order[next_index]

                # Save left turn as negative because
                counter += -1
                # Move forward while there is no wall
                while currCell not in maze.getExits() or counter != 0:
                    currCell = currCell + self.directions[currDirection]
                while currCell not in maze.getExits() or counter != 0:
                    # Get opposite direction (which cell you came from)
                    current_index = self.direction_order.index(currDirection)
                    next_index = (current_index + 3) % len(self.direction_order)
                    currDirection = self.direction_order[next_index]

                    # Check wall one rotation to the right, change this to change which wall to follow
                    current_index = self.direction_order.index(currDirection)
                    next_index = (current_index + 1) % len(self.direction_order)
                    currDirection = self.direction_order[next_index]
                    # While cannot move forward
                    while (currCell + self.directions[currDirection]) not in possibleNeighs:
                        # Check wall one rotation to the right, change this to change which wall to follow
                        current_index = self.direction_order.index(currDirection)
                        next_index = (current_index + 1) % len(self.direction_order)
                        currDirection = self.direction_order[next_index]

                    # Move forward if there is no wall
                    currCell = currCell + self.directions[currDirection]

        # ensure we are currently at the exit
        if currCell in maze.getExits():
            # append exit cell to solverPath
            self.solverPathAppend(currCell)
            self.solved(entrance, currCell)