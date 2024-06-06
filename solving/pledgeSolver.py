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

    def __init__(self):
        super().__init__()
        self.m_name = "pledge"
        self.directions = {
            'NORTH': Coordinates3D(0, 0, -1),
            'NORTH_EAST': Coordinates3D(1, 0, 0),
            'EAST': Coordinates3D(0, 1, 0),
            'SOUTH': Coordinates3D(0, 0, 1),
            'SOUTH_WEST': Coordinates3D(-1, 0, 0),
            'WEST': Coordinates3D(0, -1, 0),
        }
        self.direction_order = ['NORTH', 'NORTH_EAST', 'EAST' , 'SOUTH', 'SOUTH_WEST', 'WEST']

    def getNoOfTurns(self, direction1, direction2, turns):
        """
        This function is used to calculate the number of turns taken from the current direction to the next direction
        So the directions that are right next to the current directions will be assigned with 0.5, and those which are two away or which is further away
        are assigned with 1. The only ones that are 1 away even though they are close by are, NORTH - WEST, SOUTH - EAST
        Parameters
        -------
        a : Coordinates3d
            This is the current direction of the solver
        b : Coordinates3d
            This is the next direction of the solver
        c : int
            This stores the number of turns that has been taken already

        This function basically assigns the number of turns that has been taken to the parameter of turns.
        """

        # From 
        if direction1 == 'NORTH': # If the current direction is 'NORTH', calculating the turns on the basis of which next direction is closer
            if direction2 == 'WEST':
                turns -= 1
            elif direction2 == 'SOUTH_WEST':
                turns -= 1.5
            elif direction2 == 'SOUTH':
                turns -= 2
            elif direction2 == 'EAST':
                turns -= 3
            elif direction2 == 'NORTH_EAST':
                turns -= 3.5
        if direction1 == 'WEST': # If the current direction is 'WEST', calculating the turns on the basis of which next direction is closer
            if direction2 == 'SOUTH_WEST':
                turns -= 0.5
            elif direction2 == 'SOUTH':
                turns -= 1
            elif direction2 == 'EAST':
                turns -= 2
            elif direction2 == 'NORTH_EAST':
                turns -= 2.5
            elif direction2 == 'NORTH':
                turns -= 3
        if direction1 == 'SOUTH_WEST': # If the current direction is 'SOUTH_WEST', calculating the turns on the basis of which next direction is closer
            if direction2 == 'SOUTH':
                turns -= 0.5
            elif direction2 == 'EAST':
                turns -= 1.5
            elif direction2 == 'NORTH_EAST':
                turns -= 2
            elif direction2 == 'NORTH':
                turns -= 2.5
            elif direction2 == 'WEST':
                turns -= 3.5
        if direction1 == 'SOUTH': # If the current direction is 'SOUTH', calculating the turns on the basis of which next direction is closer
            if direction2 == 'EAST':
                turns -= 1
            elif direction2 == 'NORTH_EAST':
                turns -= 1.5
            elif direction2 == 'NORTH':
                turns -= 2
            elif direction2 == 'WEST':
                turns -= 3
            elif direction2 == 'SOUTH_WEST':
                turns -= 3.5
        if direction1 == 'EAST': # If the current direction is 'EAST', calculating the turns on the basis of which next direction is closer
            if direction2 == 'NORTH_EAST':
                turns -= 0.5
            elif direction2 == 'NORTH':
                turns -= 1
            elif direction2 == 'WEST':
                turns -= 2
            elif direction2 == 'SOUTH_WEST':
                turns -= 2.5
            elif direction2 == 'SOUTH':
                turns -= 3
        if direction1 == 'NORTH_EAST': # If the current direction is 'NORTH_EAST', calculating the turns on the basis of which next direction is closer
            if direction2 == 'NORTH':
                turns -= 0.5
            elif direction2 == 'WEST':
                turns -= 1.5
            elif direction2 == 'SOUTH_WEST':
                turns -= 2
            elif direction2 == 'SOUTH':
                turns -= 2.5
            elif direction2 == 'EAST':
                turns -= 3.5
            
    def rotate(self, direction):
        """
        This function is used basically to rotate. Taking in the current direction and the amount of rotations needed with the paramater as count,
        this function returns a value from the directions order which will be the rotation that has to be taken.

        Parameters
        -------
        a : Coordinates3d
            This is the current direction of the solver
        b : int
            These mention the amount of turns that has to be taken

        Returns
        -------
        The direction after the number of turns are taken, if the current direction is 'NORTH' and the number of turns are 3 (for a 180 degree turn),
        this function will return 'SOUTH'.
        """
        current_index = self.direction_order.index(direction)
        next_index = (current_index - 1) % len(self.direction_order)
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
        self.m_solver = False
        #Choosing a random direction from the list of directions as the preffered direction
        prefDirection = choice(self.direction_order)
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
                                                    
            # If the turns are 0, that means we are heading to our prefered direction, and if that particular direction is also a non wall path, go to that path
            while turns == 0 and ((currCell + self.directions[prefDirection]) in validNeighbours):
                    currCell = currCell + self.directions[prefDirection]
                    self.solverPathAppend(currCell)
                    validNeighbours = self.possibleNeighbours(maze, currCell) #Now find the possible neighbours of the new current cell
                    
            # When we encounter a wall in our prefered direction, we enter to the wall following algorithm.
            # This while loop just does an 180 degree turn and then gets the number of turns as we turned left thrice.
            while count < 3:
                self.getNoOfTurns(currDirection, self.rotate(currDirection), turns)
                currDirection = self.rotate(currDirection)
                count += 1
            count = 0

            # Then we check the left wall to see if it is possible to go in that direction.
            # Again getting the turns as we are turning left again.
            self.getNoOfTurns(currDirection, self.rotate(currDirection), turns)
            currDirection = self.rotate(currDirection)

            # If the particular direction is also a wll, we turn till we find a direction that has no wall.
            while (currCell + self.directions[currDirection]) not in validNeighbours:
                 # Again getting the turns as we are turning left again.
                self.getNoOfTurns(currDirection, self.rotate(currDirection), turns)
                currDirection = self.rotate(currDirection)
            
            # When it is possible to go into a direction that has no walls, we move there
            currCell = currCell + self.directions[currDirection]

            """
            Adding this amount as this will take in account for the number of right turns we take.  
            Suppose we are turning from 'NORTH' to 'WEST', we will be taking '-1' turns (left turn). Adding 4 which is sum of all the directions 
            will give '3' turns which is the amount of right turns that has to be taken
            """
            turns += 4  
                
        #If we are at the exit right now, add that particular cell to the path and declare that the maze has been solved
        if currCell in maze.getExits():
            self.solverPathAppend(currCell, False)
            self.solved(entrance, currCell)

        