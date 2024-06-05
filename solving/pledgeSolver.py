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
        if direction1 == 'NORTH':
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
        if direction1 == 'WEST':
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
        if direction1 == 'SOUTH_WEST':
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
        if direction1 == 'SOUTH':
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
        if direction1 == 'EAST':
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
        if direction1 == 'NORTH_EAST':
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
        current_index = self.direction_order.index(direction)
        next_index = (current_index - 1) % len(self.direction_order)
        return self.direction_order[next_index]
    
    def possibleNeighbours(self, maze: Maze3D, currCell: Coordinates3D):
        neighbours : list[Coordinates3D] = maze.neighbours(currCell)
        possibleNeighs: list[Coordinates3D] = [ neigh for neigh in neighbours if not maze.hasWall(currCell, neigh) and \
                                                   (neigh.getRow() >= 0) and (neigh.getRow() <= maze.rowNum(neigh.getLevel())) \
                                                    and (neigh.getCol() >= 0) and (neigh.getCol() <= maze.colNum(neigh.getLevel())) ]
        return possibleNeighs
                
    def solveMaze(self, maze: Maze3D, entrance: Coordinates3D):
        self.m_solver = False
        prefDirection = choice(self.direction_order)
        currDirection = prefDirection
        currCell: Coordinates3D = entrance 
        turns : int = 0 
        count : int = 0

        while currCell not in maze.getExits():
            self.solverPathAppend(currCell)

            validNeighbours = self.possibleNeighbours(maze, currCell)
                                                    
            
            while turns == 0 and ((currCell + self.directions[prefDirection]) in validNeighbours):
                    currCell = currCell + self.directions[prefDirection]
                    self.solverPathAppend(currCell)
                    validNeighbours = self.possibleNeighbours(maze, currCell)
                    
            while count < 3:
                self.getNoOfTurns(currDirection, self.rotate(currDirection), turns)
                currDirection = self.rotate(currDirection)
                count += 1
            count = 0

            self.getNoOfTurns(currDirection, self.rotate(currDirection), turns)
            currDirection = self.rotate(currDirection)

            while (currCell + self.directions[currDirection]) not in validNeighbours:
                self.getNoOfTurns(currDirection, self.rotate(currDirection), turns)
                currDirection = self.rotate(currDirection)
            
            currCell = currCell + self.directions[currDirection]
            turns += 4 # Will account for right turns
                
        
        if currCell in maze.getExits():
            self.solverPathAppend(currCell, False)
            self.solved(entrance, currCell)

        