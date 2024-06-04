# -------------------------------------------------------------------
# DON'T CHANGE THIS FILE.
# Prim's maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from random import randint, choice
from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator



class PrimMazeGenerator(MazeGenerator):
    """
    Prim's algorithm maze generator.  
    """

    def generateMaze(self, maze: Maze3D):
        maze.initCells(True)

        # select starting cell 
		# random floor
        startLevel = randint(0, maze.levelNum() - 1)
        startCoord = Coordinates3D(startLevel, randint(0, maze.rowNum(startLevel) - 1), randint(0, maze.colNum(startLevel) - 1))
        
        currCell : Coordinates3D = startCoord #the current cell is the starting random cell we selected
        visited : set[Coordinates3D] = set([currCell]) # creating a visited set and adding the current cell into it as it has been already visited

        # a list for the frontier cells
        frontier : list[Coordinates3D] = []

        # adding the initial neighbours of the current cell which are within the boundary to the frontier set
        neighbours = maze.neighbours(currCell)
        nonVisitedNeighs : list[Coordinates3D] = [neigh for neigh in neighbours if neigh not in visited and\
											 neigh.getRow() >= 0 and neigh.getRow() < maze.rowNum(neigh.getLevel()) and\
												neigh.getCol() >= 0 and neigh.getCol() < maze.colNum(neigh.getLevel())]
        for neigh in nonVisitedNeighs:
            frontier.append((currCell, neigh))

        # Executing this until the frontier set is empty
        while frontier:
            # selecting random cell pair to start with. (Initially the current cell itself will be chosen as it is the only 'fromCell' added)
            fromCell, toCell = choice(frontier)
            frontier.remove((fromCell, toCell)) #After selection, the cell pair has been removed from the set

            if toCell not in visited: # If the toCell has not been visited
                visited.add(toCell) # Add toCell to the maze
                maze.removeWall(fromCell, toCell) # Knock down the wall between fromCell and toCell
                currCell = toCell # Update the current cell

                # Add the neighbors of the new cell to the frontier set if they have not been visited and within the maze boundaries
                newNeighbours = maze.neighbours(currCell)
                nonVisitedNeighs : list[Coordinates3D] = [neigh for neigh in newNeighbours if neigh not in visited and\
											 neigh.getRow() >= 0 and neigh.getRow() < maze.rowNum(neigh.getLevel()) and\
												neigh.getCol() >= 0 and neigh.getCol() < maze.colNum(neigh.getLevel())]
                for newNeigh in nonVisitedNeighs:
                    if newNeigh not in visited:
                        frontier.append((currCell, newNeigh))

        # update maze generated
        self.m_mazeGenerated = True