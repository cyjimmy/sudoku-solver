# COMP3981 Sudoku Solver
Solve sudoku using some algorithms (ง︡'-'︠)ง

## How To Run
1. Install Python version 3.10
2. Install project dependencies
```buildoutcfg
pip install -r requirements.txt
```
3. Run the /frontend/driver.py file

## Sudoku Solving Algorithms
#### Algorithm File Location
```buildoutcfg
/frontend/sudoku_solver.py
```
### Brute Force
1. The algorithm will try and find a cell with the least amount of possible options.
2. Given the cell with the least amount of options it will select a random value and assign it to the cell.
3. Then repeat step 1 and 2 recursively until no cells are returned from step 1.
4. If no cells are returned from step 1 then check if the board is solved.
5. If the board is not solved back track to previous cell and select another random value from the list to try.

Note: Given that it randomly selects values from the possible list of values to try we have a timeout for each board size.
Once the timeout is reached, the algorithm will retry from the start again in hopes that it may get lucky and find a
solution by selecting a different random value for the first cell.

### CSP