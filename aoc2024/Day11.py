import time
import Utils
from aocd import submit

day = 11
year = 2024
p1_expected_tst_result = 55312
p2_expected_tst_result = 65601038650482

Utils.download_input(year, day)


def add(temp_solution, stone_id, n):
    temp_solution[stone_id] = temp_solution.get(stone_id, 0) + n


def step(temp_solutions, solution):
    stone_id, n = solution

    if stone_id == 0:
        add(temp_solutions, 1, n)
    else:
        s = str(stone_id)
        q, r = divmod(len(s), 2)
        if r == 0:
            add(temp_solutions, int(s[:q]), n)
            add(temp_solutions, int(s[q:]), n)
        else:
            add(temp_solutions, stone_id * 2024, n)


def solve(data, k=25):
    solutions = {int(x): 1 for x in data.split()}
    for _ in range(k):
        temp_solutions = {}
        for solution in solutions.items():
            step(temp_solutions, solution)

        solutions = temp_solutions

    return sum(solutions.values())

if __name__ == "__main__":
    tst_input = Utils.read_input_flat(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input_flat(f"input/day{day}_input.txt")

    print("Part 1")
    start_time = time.time()
    p1_tst_result = solve(tst_input)
    print(f"Test solution: {p1_tst_result}.")
    elapsed_time = time.time() - start_time
    print(f"Time taken p1 test: {elapsed_time:.2f} seconds")
    if p1_tst_result == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p1_result = solve(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p1: {elapsed_time:.2f} seconds")
        submit(p1_result, part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    start_time = time.time()
    p2_tst_result = solve(tst_input, 75)
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p2_result = solve(puzzle_input, 75)
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
