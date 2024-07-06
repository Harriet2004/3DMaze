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
    Pledge solver implementation.  
    """

    def __init__(self):
        super().__init__()
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

    def getNoOfTurns(self, prevDirection, destDirection):
        """
        This function is used to calculate the number of turns taken from the current direction to the next direction
        Parameters
        -------
        a : Coordinates3d
            This is the current direction of the solver
        b : Coordinates3d
            This is the next direction of the solver

        Returns
        -------
        int
            This is the number of turns that are taken
        """

        # From 
        if prevDirection == 'NORTH': # If the current direction is 'NORTH', calculating the turns on the basis of which next direction is closer
            if destDirection == 'WEST':
                return 1
            elif destDirection == 'SOUTH_WEST':
                return 2
            elif destDirection == 'SOUTH':
                return 3
            elif destDirection == 'EAST':
                return -2
            elif destDirection == 'NORTH_EAST':
                return -1
        if prevDirection == 'WEST': # If the current direction is 'WEST', calculating the turns on the basis of which next direction is closer
            if destDirection == 'SOUTH_WEST':
                return 1
            elif destDirection == 'SOUTH':
                return 2
            elif destDirection == 'EAST':
                return 3
            elif destDirection == 'NORTH_EAST':
                return -2
            elif destDirection == 'NORTH':
                return -1
        if prevDirection == 'SOUTH_WEST': # If the current direction is 'SOUTH_WEST', calculating the turns on the basis of which next direction is closer
            if destDirection == 'SOUTH':
                return 1
            elif destDirection == 'EAST':
                return 2
            elif destDirection == 'NORTH_EAST':
                return 3
            elif destDirection == 'NORTH':
                return -2
            elif destDirection == 'WEST':
                return -1
        if prevDirection == 'SOUTH': # If the current direction is 'SOUTH', calculating the turns on the basis of which next direction is closer
            if destDirection == 'EAST':
                return 1
            elif destDirection == 'NORTH_EAST':
                return 2
            elif destDirection == 'NORTH':
                return 3
            elif destDirection == 'WEST':
                return -2
            elif destDirection == 'SOUTH_WEST':
                return -1
        if prevDirection == 'EAST': # If the current direction is 'EAST', calculating the turns on the basis of which next direction is closer
            if destDirection == 'NORTH_EAST':
                return 1
            elif destDirection == 'NORTH':
                return 2
            elif destDirection == 'WEST':
                return 3
            elif destDirection == 'SOUTH_WEST':
                return -2
            elif destDirection == 'SOUTH':
                return -1
        if prevDirection == 'NORTH_EAST': # If the current direction is 'NORTH_EAST', calculating the turns on the basis of which next direction is closer
            if destDirection == 'NORTH':
                return 1
            elif destDirection == 'WEST':
                return 2
            elif destDirection == 'SOUTH_WEST':
                return 3
            elif destDirection == 'SOUTH':
                return -2
            elif destDirection == 'EAST':
                return -1
            
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
    
    def possibleNeighbours(self, maze: Maze3D, currCell: Coordinates3D):
        """
        This function is used to find the neighbours that can be visited (basically which are not walls as well)
        Parameters
        -------
        a : Maze3D
            This is used to use methods like neighbours, hasWall etc.
        b : Coordinates3D
            This passes the current cell so that the neighbours of the cell can be calculated and filtered

        Returns
        -------
        list
            The list of possible neighbours that can be visited
        """
        neighbours : list[Coordinates3D] = maze.neighbours(currCell)
        possibleNeighs: list[Coordinates3D] = [ neigh for neigh in neighbours if not maze.hasWall(currCell, neigh) and \
                                                   (neigh.getRow() >= -1) and (neigh.getRow() <= maze.rowNum(neigh.getLevel())) \
                                                    and (neigh.getCol() >= -1) and (neigh.getCol() <= maze.colNum(neigh.getLevel())) ]
        return possibleNeighs
                
    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        """
        In this wall follower, we are turning left so we are following right hand wall follower
        """

        self.m_solver = False
        #Choosing a random direction from the list of directions as the preffered direction
        prefDirection = choice(self.direction_order)
        print(prefDirection)
        #Assigning that as the current direction for later use (wall following part)
        currDirection = prefDirection
        # select starting cell
        currCell: Coordinates3D = entrance 

        turns : int = 0 # This is the number of turns that are going to be taken once the pledge enters the wall following algorithm
        count : int = 0 # This is just a random counter that will be used in this solver

        while currCell not in maze.getExits():
            # append the current cell visited
            self.solverPathAppend(currCell)
            # This is calling the function that grabs the possible (valid neighbours of the current cell which are not walls)
            validNeighbours = self.possibleNeighbours(maze, currCell)
                                                    
            # If the turns are 0, that means we are heading to our preferred direction, and if that particular direction is also a non wall path, go to that path
            while turns == 0 and ((currCell + self.directions[prefDirection]) in validNeighbours):
                currCell = currCell + self.directions[prefDirection]
                self.solverPathAppend(currCell)
                validNeighbours = self.possibleNeighbours(maze, currCell) #Now find the possible neighbours of the new current cell
                    
            # When we encounter a wall in our preferred direction, we enter to the wall following algorithm.
            # This while loop just does an 180 degree turn
            while count < 3:
                currDirection = self.rotate(currDirection,3)
                count += 1
            count = 0

            # Then we check the left wall to see if it is possible to go in that direction.
            # Getting the no of turns
            currDirection = self.rotate(currDirection,1)
            turns += self.getNoOfTurns(currDirection, self.rotate(currDirection,1))


            # If the particular direction is also a wall, we turn till we find a direction that has no wall.
            while (currCell + self.directions[currDirection]) not in validNeighbours:
                 # Again getting the turns as we are turning left again.
                turns += self.getNoOfTurns(currDirection, self.rotate(currDirection,1))
                currDirection = self.rotate(currDirection,1)
            
            # When it is possible to go into a direction that has no walls, we move there
            currCell = currCell + self.directions[currDirection]
                
        #If we are at the exit right now, add that particular cell to the path and declare that the maze has been solved
        if currCell in maze.getExits():
            self.solverPathAppend(currCell, False)
            self.solved(entrance, currCell)

        