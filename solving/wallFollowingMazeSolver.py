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
        # Defining directions that are going to be used
        self.directions = {
            'NORTH': Coordinates3D(0, 1, 0),
            'NORTH_EAST': Coordinates3D(1, 0, 0),
            'EAST': Coordinates3D(0, 0, 1),
            'SOUTH': Coordinates3D(0, -1, 0),
            'SOUTH_WEST': Coordinates3D(-1, 0, 0),
            'WEST': Coordinates3D(0, 0, -1),
        }
        # The order of directions for the solver to refer to
        self.direction_order = ['NORTH', 'NORTH_EAST', 'EAST' , 'SOUTH', 'SOUTH_WEST', 'WEST']

    def rotate(self, direction, count):
        """
        This function is used basically to rotate. Taking in the current direction and the amount of rotations needed with the paramater as count,
        this function returns a value from the directions order which will be the rotation that has to be taken.

        Parameters
        -------
        a : Coordinates3D
            This is the current direction of the solver
        b : int
            These mention the amount of turns that has to be taken

        Returns
        -------
        Coordinates3D
            The direction after the number of turns are taken.
        """
        current_index = self.direction_order.index(direction) #grabs the current index of the current direction from the directions list
        next_index = (current_index - count) % len(self.direction_order) # calculate the number of turns from the current index and assigns to the next index
        return self.direction_order[next_index]

    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        """
        In this wall follower, we are turning left so we are following right hand wall follower
        """

        self.m_solved = False 
        	
        # select starting cell
        currCell: Coordinates3D = entrance
        # selecting a particular direction to start from initially, in this case 'NORTH' is chosen
        currDirection = 'NORTH'

        while currCell not in maze.getExits():
            # append the current cell visited
            self.solverPathAppend(currCell)

            # Getting the list of neighbours of the current cells
            neighbours : list[Coordinates3D] = maze.neighbours(currCell)

            # Getting the list of neighbours that can be visited (which are not walls)
            possibleNeighs: list[Coordinates3D] = [ neigh for neigh in neighbours if not maze.hasWall(currCell, neigh) and \
                                                   (neigh.getRow() >= -1) and (neigh.getRow() <= maze.rowNum(neigh.getLevel())) \
                                                    and (neigh.getCol() >= -1) and (neigh.getCol() <= maze.colNum(neigh.getLevel())) ]


            # getting the direction that the solver came from (180 degree turn)
            currDirection = self.rotate(currDirection,3)

            # Checking one wall to the left (following right-wall follower)
            currDirection = self.rotate(currDirection,1)
            # If it is not possible to move forward, we continously check to our left
            while (currCell + self.directions[currDirection]) not in possibleNeighs:
                currDirection = self.rotate(currDirection,1)

            # Moving forward if there is no wall ahead and carry on
            currCell = currCell + self.directions[currDirection]

        #If we are at the exit right now, add that particular cell to the path and declare that the maze has been solved
        if currCell in maze.getExits(): 
            self.solverPathAppend(currCell)
            self.solved(entrance, currCell)