# COMP3981 Sudoku Solver
Solve sudoku using some algorithms (ง︡'-'︠)ง

## How To Run
1. Install Python version 3.10
2. Install project dependencies
```buildoutcfg
pip install -r requirements.txt
```
3. Run the /frontend/driver.py file

### Puzzle Generation
1. Script-based random generation (for puzzles 12x12 or less)
   1. Generate random values for the diagonal
   2. Fill in the rest (up to 25%) using the brute force algorithm
2. File-based random generation (for puzzles 16x16 or more)
   1. Pick a random solved puzzle with the desired size
   2. Remove the values randomly until 75% of cells is empty
3. Loading a file containing a puzzle

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
1. Preparation
   1. Find empty cells
   2. Identify arcs
   3. Find all empty cells' domains
2. Backtracking Search
   1. MRV and Degree Heuristic for variable selection
   2. Least-Constraining-Value Heuristic for value ordering
   3. MAC for inference
3. Multiprocessing

###### Preparation
```angular2html
    def solve(self, board: list, start_time, limit=SOLVE_TIME_LIMIT):
        self._reset()
        self._start_time = time.time()
        self._terminate_time = time.time() + limit
        self._board = board
        self._size = len(self._board)
        self._find_empty_cells()
        self._find_related_cells()
        self._get_initial_domains()
        return self._fill_cell()
```
A list of functions are called before the backtracking search starts. `solve` is the entry point of the csp algorithm. `_fill_cell` is the actual backtracking search. In preparation, we store mandatory information such as empty cells and domains as class attributes. There are some other information we found beneficial to store before the search as it reduces repetitive calculation. Some examples are the grid value of each empty cells, and emtpy cells for certain row, column, or grid.

###### Identify Arcs
After getting all the empty cells, we check if those cells are related (in the same row, column or grid), if they do, we store it as an arc in a dictionary.

###### MRV and Degree Heuristic
We use MRV to pick the empty cell for assignment. In `_mrv` function, we find the empty cell with the least domain. We store that into a result list, if the list has more than one item, it means there is a tie.

To solve the tie, `-mrv` function will call `_degree_heuristic` function. This will identify the cell with most related cells which also means a higher degree.

Note: For large size puzzle, there will be tie even after applying degree heuristic. Since the data structure we use is `set`, this will introduce unintentional randomness to the algorithm.

###### Least-Constraining-Value Heuristic
To order the value for assignment, we have the `_arrange_value` function which counts the occurrence of each value in empty cells' domains. This does not check all the empty cells, but only those that are related to the cell we picked in previous step. The values are arranged in ascending order.

###### MAC
We also check arc consistency whenever a cell is assigned a value. The `_ac_3` function first generates a queue with all the arcs of the assigned cell. Then it calls `_revise`. The `_revise` function updates the domain of variables. If any variable's domain get updated, the function returns True. If `_revise` returns True, `_ac_3` will check if domain size is reduced to 0, if it is, function returns False, backtracking search will backtrack. If domain size is not 0, `_ac_3` adds corresponding arc into queue. 

###### Sudoku Technique (Unique Candidate)
When the `_revise` function updates domain of empty cells, it will call `_update_unique_candidate`. We wrote this function based on a technique calls Unique Candidate.

Unique Candidate means if in a given row, there is only one cell which can hold a specific value, the cell must be that value.

```
self._empty_cells_in_rows = {}
self._empty_cells_in_cols = {}
self._empty_cells_in_grids = {}
```

To implement this sudoku technique, we also modify the preparation process and save the attributes above before backtracking. This can reduce unnecessary calculation during search.

Reference: `https://sudoku.com.au/QXI13-2-1992-0-Unique-Candidate-Technique-Exp.aspx`

###### Multiprocessing
As mentioned above, there is randomness in the algorithm, that is why we think the performance can be improved using multiprocessing. Our approach is fairly simple, we create a process pool, then each process will create a new instance of CSP solver and try to solve the puzzle.

After some benchmarking, we found out only size 25 or above will be improved using multiprocessing. Since the performance for smaller puzzles are pretty good, implementing multiprocessing will only add unnecessary overheads.

### Statistics
#### Brute Force
|       | Average time (seconds) | Standard deviation | Success |
|-------|------------------------|--------------------|---------|
| 9x9   | 0.06772525             |0.19890018 | 15/15|
| 12x12 | 3.5306933           |6.14235701 | 15/15|
| 16x16 | 19.2738021           |20.8148636 | 15/15|
| 25x25 | 144.814612           |67.8336156 | 6/15|

#### CSP
|       | Average time (seconds) | Standard deviation | Success |
|-------|------------------------|--------------------|---------|
| 9x9   | 0.0349             |0.0720 | 15/15   |
| 12x12 | 0.0349           |0.0117 | 15/15   |
| 16x16 | 0.5071          |1.2454 | 15/15   |
| 25x25 | 13.7136           |25.4175 | 14/15   |
