# -------------------------------------------------------------------
# PLEASE UPDATE THIS FILE.
# Task C solver.
#
# _author_ = 'Jeffrey Chan'
# _copyright_ = 'Copyright 2024, RMIT University'
# -------------------------------------------------------------------


from maze.maze3D import Maze3D
from solving.mazeSolver import MazeSolver
from maze.util import Coordinates3D



class TaskCMazeSolver(MazeSolver):
    """
    Task C solver implementation.  You'll need to complete its implementation for task C.
    """


    def __init__(self):
        super().__init__()
        self.m_name = "taskC"
        self.directions = {
            'NORTH': Coordinates3D(0, 1, 0),
            'NORTH_EAST': Coordinates3D(1, 0, 0),
            'EAST': Coordinates3D(0, 0, 1),
            'SOUTH': Coordinates3D(0, -1, 0),
            'SOUTH_WEST': Coordinates3D(-1, 0, 0),
            'WEST': Coordinates3D(0, 0, -1),
        }
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
            The direction after the number of turns are taken, if the current direction is 'NORTH' and the number of turns are 3 (for a 180 degree turn),
            this function will return 'SOUTH'.
        """
        current_index = self.direction_order.index(direction) #grabs the current index of the current direction from the directions list
        next_index = (current_index - count) % len(self.direction_order) # calculate the number of turns from the current index and assigns to the next index
        return self.direction_order[next_index]
        
        
    def possibleNeighbours(self, maze: Maze3D, currCell: Coordinates3D, exits: list[Coordinates3D]):
        """
        This function is used to find the neighbours that can be visited (basically which are not walls as well) and making sure they are not the
        exits as well
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
                                                    and (neigh.getCol() >= -1) and (neigh.getCol() <= maze.colNum(neigh.getLevel())) and neigh not in exits ]
        return possibleNeighs
    
    def getUniqueCellCount(self, path: list[Coordinates3D]):
        """
        This function is used to get the number of unique cells in the particular path
        -------
        a : list[Coordinates3D]
            This is the path from which the unique cells are going to be found
        Returns
        -------
        int
            The size of the path which has all cells unique(explored only once)
        """
        uniquePath: list[Coordinates3D] = list()
        for cell in path: # Checking each cell in the path 
            if cell not in uniquePath: 
                uniquePath.append(cell) # Adding the cell into the unique path if it does not exist in it
        return len(uniquePath)
    
    def getPathFromEachEntrance(self, entrance: Coordinates3D, maze: Maze3D, paths: list[list[Coordinates3D]]):
        """
        This function is used to get the paths/path from a particular entrance
        Parameters
        -------
        a : Coordinates3D
            This is the entrance that is used to find the path
        b : Maze3D
            This is used to use methods like neighbours, hasWall etc.
        c : list[list[Coordinates3D]]
            This is the list of paths that has to be returned later with more paths
        Returns
        -------
        list[list[Coordinates3D]]
            The list of paths after checking the paths from the current entrance
        """
        exits: list[Coordinates3D] = list() #List to store the explored exits
        mazeExitsCount: int = len(maze.getExits()) # Getting the number of exits that exist for the entrance to reach
        while len(exits) < mazeExitsCount: # The loop will run until the entrances find the paths to all the exits
            path: list[Coordinates3D] = list() 
            currCell = entrance # Current cell is the entrance to start with 
            goDirection = 'NORTH' # Direction to go is set as 'NORTH'
            while currCell not in maze.getExits():
                path.append(currCell)
                # Getting the list of neighbours of the current cells
                possibleNeighs = self.possibleNeighbours(maze,currCell,exits)

                # getting the direction that the solver came from (180 degree turn)
                goDirection = self.rotate(goDirection,3)

                # Checking one wall to the left (following right-wall follower)
                goDirection = self.rotate(goDirection,1)
                # If it is not possible to move forward, we continously check to our left
                while (currCell + self.directions[goDirection]) not in possibleNeighs:
                    goDirection = self.rotate(goDirection,1)

                # Moving forward if there is no wall ahead and carry on
                currCell = currCell + self.directions[goDirection]
            """
            Checking whether the current cell has reached an exit. Not using the getExits() to navigate through the maze but just 
            to see if the cell is in an exit or not
            """
            if currCell in maze.getExits():
                path.append(currCell) # Adds the current cell to the path
                paths.append(path) # Adds the current path to the list of paths
                exits.append(currCell) # Adds the current exit to the list of exits
                
        return paths 
    
    def getShortestPath(self, paths: list[list[Coordinates3D]], maze: Maze3D):
        """
        This function is used to find the path with all additional cells remove. Additional cells here means that if the wall follower goes through
        a loop, the cells of the loop will be removed and a new path will be formed. Then the function will find the number of cells of the path 
        and then print that in the terminal
        -------
        a : list[list[Coordinates3D]]
            This the list of paths that has to be checked to find the minimum path
        b : Maze3D
            This is used to use methods like neighbours, hasWall etc.
        Returns
        -------
        list[Coordinates3D]
            The list of the path with the least cells
        """
        cellsOfLeastPath = None # Having an integer to store the number of cells for the path with least number of cells
        smallPath: list[Coordinates3D] = list() # Having a list to store the smallest path (least number of cells)

        for path in paths:
            loopFreePath = self.loopRemover(path) # Calling the function to remove the loops
            cellsOfPath = self.getCountOfUniqueCells(loopFreePath) # Counting the number of unique cells in the path
            # This prints the path and the number of cells in the terminal
            print('Entrance:', loopFreePath[0], 'Exit:', loopFreePath[-1], 'with cells:', cellsOfPath)

            if cellsOfLeastPath is None or cellsOfPath < cellsOfLeastPath: # Checking if there is another path smaller than one of the least paths
                # Assigning that path as the path with least number of cells
                cellsOfLeastPath = cellsOfPath
                smallPath = loopFreePath
        return smallPath


    def loopRemover(self, path: list[Coordinates3D]):
        """
        This function is used to remove the loops of the particular path. For an solver like wall follower, it can go through the same cell twice
        depending on which wall it follows. So if there are loops, it will remove it to find the number of unique cells
        Parameters
        -------
        a : list[Coordinates3D]
            This is the list of the path
        Returns
        -------
        list[Coordinates3D]
            This is the list of the loopFreePath with no loops
        """
        loopFreePath: list[Coordinates3D] = list() # The path with no loops
        for cell in path:
            if cell in loopFreePath:
                # Similarly to the wilson's algorithm, this will find the index of the cell which is repeating (causing the loop)
                loop_index = loopFreePath.index(cell)
                # Then the loopFreePath will slice the list to that particular cell, so the cells after that which causes loop will be removed
                loopFreePath = loopFreePath[:loop_index + 1]
            else:
                loopFreePath.append(cell) # If there are no repeating cells, we just add the cell to the loopFreePath

        return loopFreePath
    
    def getCountOfUniqueCells(self, path: list[Coordinates3D]):
        """
        This function is used to find the number of unique cells explored
        Parameters
        -------
        a : list[Coordinates3D]
            This is the list from which the length will be found
        Returns
        -------
        int
            The number of unique cells explored in this path
        """

        temp: list[Coordinates3D] = list() # Creating a temporary path to see if cells are unique or not in the path passed as parameter
        for cell in path:
            if cell not in temp: # For each cell in the path, if the cell is not repeating in the temporary path, we add it to that list
                temp.append(cell) 
                
        return len(temp)
    
    def solveMaze(self, maze: Maze3D):
        # we call the the solve maze call without the entrance.
        # DO NOT CHANGE THIS METHOD
        self.solveMazeTaskC(maze)
    
    def solveMazeTaskC(self, maze: Maze3D):
        self.m_solved = False

        #Getting the list of entrances of the maze
        mazeEntrances : list[Coordinates3D] = maze.getEntrances()
        # Making a nested list to store the paths from the entrance/entrances to the exit/exits
        mazePaths : list[list[Coordinates3D]] = [path for path in []]
        
        # For each entrance of the maze, finding a path from it to the exit of the maze and adding it to the main list of mazePaths
        for entrance in mazeEntrances:
            mazePaths + [self.getPathFromEachEntrance(entrance,maze,mazePaths)]

        # Finding the path with the least number of cells and declaring that as the path that has been used to solve the maze
        minPath = self.getShortestPath(mazePaths,maze)
        print("The path with the least number of cells is:", len(minPath))

        for currCell in minPath:
            self.solverPathAppend(currCell)
            self.solved(minPath[0], minPath[-1])