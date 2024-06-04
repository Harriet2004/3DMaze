# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Wilson's algorithm maze generator.
#
# __author__ = 'Jeffrey Chan'
# __copyright__ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------

from random import randint,choice
from maze.maze3D import Maze3D
from maze.util import Coordinates3D
from generation.mazeGenerator import MazeGenerator


class WilsonMazeGenerator(MazeGenerator):
    """
    Wilson algorithm maze generator.
    """
    def generateMaze(self, maze: Maze3D):
        # make sure we start the maze with all walls there
        maze.initCells(True) 

        # select starting cell 
		# random floor
        startLevel = randint(0, maze.levelNum() - 1)
        startCoord = Coordinates3D(startLevel, randint(0, maze.rowNum(startLevel) - 1), randint(0, maze.colNum(startLevel) - 1))

        
        finalised : set[Coordinates3D] = set([startCoord]) #creating a finalsed set which contains the cells that are all visited and finalised
        unvisited : set[Coordinates3D] = set() #creating an unvisited set to choose the cells from and later mark them finalised.
        #making nested for loops so that each cell of the maze can be added to the unvisited set.
        for level in range(maze.levelNum()):
            for row in range(maze.rowNum(level)):
                for col in range(maze.colNum(level)):
                    coord = Coordinates3D(level, row, col)
                    if coord != startCoord: # as the start coordinate is already finalised and visited, it is not being added to the unvisited set
                        unvisited.add(coord) 

        while unvisited:
            # Choosing a random cell from the unvisited set until its empty
            currentCell = choice(list(unvisited))
            path : list[Coordinates3D] = [currentCell] # Having a path to store the cell path
            path_track : set[Coordinates3D] = set([currentCell]) # Having a set to track the path for loops not to occur
            
            # Perform a random walk until a visited cell is reached
            while currentCell not in finalised:
                validNeighbours : list[Coordinates3D] = [] # Having a list to store the neighbours that are within the boundary and are valid
                neighbours = maze.neighbours(currentCell) # Now checking the neighbours of the currentCell that is chosen
                for neigh in neighbours:
                    if neigh.getRow() >= 0 and neigh.getRow() < maze.rowNum(neigh.getLevel()) and\
						neigh.getCol() >= 0 and neigh.getCol() < maze.colNum(neigh.getLevel()):
                        validNeighbours.append(neigh) # Adding all the valid neighbours to the main list.
                
                nextCell = choice(validNeighbours) # Choosing one of the valid neighbours as the next cell

                """ 
                If the path has any loops, that means it has one cell repeating twice. So having a check for that 
                Removing the elements from the path until the first instance of the cell is met. After the first
                instance of the cell, the path following would be the one causing the loop so removing that to remove
                the loop
                """
                if nextCell in path_track: # If the cell is already there in the path 
                    while path and path[-1] != nextCell : # Checking until the first instance of the cell is met and the path is not empty
                        endingCell = path.pop() # Getting the last cell of the path 
                        path_track.remove(endingCell) # Removing the last cell
                else:
                    path.append(nextCell) #If a loop will not be caused, then just appending the cell to the path
                    path_track.add(nextCell)
                    
                currentCell = nextCell # Changing the value of the currentCell with the nextCell to carry on the loop and path

            # This for loop is used to carve the path that has been formed.
            for i in range(len(path) - 1):
                prevCell = path[i]
                nextCell = path[i + 1]
                maze.removeWall(prevCell, nextCell)

            # After everything, each cell in the path is added to the finalised set.
            for cell in path:
                finalised.add(cell)
                if cell in unvisited: # If there is any cell existing in the unvisited cell, removing as it everything has been added to the finalised.
                    unvisited.remove(cell)
        
        # update maze generated
        self.m_mazeGenerated = True
    
		
        
        
		