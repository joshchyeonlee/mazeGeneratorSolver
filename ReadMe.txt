mazeSolver.py README

Project inspired by https://www.youtube.com/watch?v=Xthh4SEMA2o&ab_channel=DavisMT

Program implements pygame.py to generate a randomized maze from a 2D matrix using a backtracking algorithm and solves the maze from the starting (top left) coordinate to the end (bottom right).

Once code is run, users can press the spacebar to see the maze being generated in real-time. Once the maze is created, the program finds the path from the start to the end automatically. Maze solving is brute forced. Once finished, the maze path solution will be printed.

WINDOW_WIDTH, WINDOW_HEIGHT, CELL_WIDTH, CELL_HEIGHT can be altered as long as cell dimensions can divide window dimensions evenly.