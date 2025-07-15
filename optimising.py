from random import random, randint, choice
from math import exp

"""
Dummy code I used to try and optimise the simulated annealing process.
Not used as part of the SudokuGame code."""

def simulated_annealing_solver(grid, initialTemp, decrease_factor):
    NUMS = set(["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    iters = 0
    temp = initialTemp
    DECREASE_FACTOR = decrease_factor
    for y in range(9):
        for x in range(9):
            if grid[y][x] == "":
                grid[y][x] = choice(list(NUMS - get3x3box(grid, x, y)))

    prev_score = get_score(grid)
    while iters < 3000:
        # Selects any two editable cells in the same 3x3 box
        valid = False
        while not valid:
            x1, y1 = randint(0, 8), randint(0, 8)
            x2, y2 = randint(x1-x1%3, x1-x1%3+2), randint(y1-y1%3, y1-y1%3+2)
            valid = editable[y1][x1] and editable[y2][x2] and (x1, y1) != (x2, y2)

        grid[y1][x1], grid[y2][x2] = grid[y2][x2], grid[y1][x1]
        iters += 1
        
        new_score = get_score(grid)

        if new_score < prev_score:
            prev_score = new_score
        elif exp(new_score - prev_score)/temp < random():
            prev_score = new_score
        else:
            grid[y1][x1], grid[y2][x2] = grid[y2][x2], grid[y1][x1]
        if prev_score == 0:
            break
        temp *= DECREASE_FACTOR
    return iters


def get_score(grid) -> int:
    score = 0
    for i in range(9):
        score += 9 - len(set(grid[i]))
    col = set()
    for x in range(9):
        for y in range(9):
            col.add(grid[y][x])
    score += 9 - len(col)
    return score

def get3x3box(grid, x, y):
    box = set()
    # Gets the x and y coordinates of the top left cell of the 3x3 box
    y = y - y%3
    x = x - x%3
    for i in range(3):
        for j in range(3):
            box.add(grid[y+i][x+j])
    return box

mygrid = [["" for x in range(9)] for y in range(9)]
editable = [[True for x in range(9)] for y in range(9)]
with open("puzzle1.txt") as puzzle:
    for y, row in enumerate(puzzle):
        for x, digit in enumerate(row):
            if digit in "123456789":
                mygrid[y][x] = digit
                editable[y][x] = False

from copy import deepcopy

initialtemp = 1
for num in range(50):
    initialtemp += 0.05
    print(f"temp: {round(initialtemp, 3)}", end="")
    results = []
    for attempt in range(2500):
        iterations = simulated_annealing_solver(deepcopy(mygrid), initialtemp, 0.999999)
        results.append(iterations)
    mean = sum(results) // len(results)
    std_dev = (sum([(x - mean)**2 for x in results]) / len(results))**0.5
    print(f", Mean iterations: {mean}, Standard Deviation: {round(std_dev, 0)}, Sum of the two = {round(mean+std_dev, 0)}")
    # I wasn't sure how to do this the most mathematically - but I figured summing the mean and standard deviation would give a good 
    # estimate of what temperature is most accurate and consistent on average for this sudoku. This ended up being temp=3.0
    # Mean iterations: 590, Standard Deviation: 367.0
    
                