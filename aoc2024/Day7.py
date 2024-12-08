import itertools
import time
import Utils
from aocd import submit

day = 7
year = 2024
p1_expected_tst_result = 3749
p2_expected_tst_result = 11387

Utils.download_input(year, day)


def solve(data, concat=False):
    equations = [d.split(": ") for d in data]

    operations = ["+", "*"]

    total = 0
    for e in equations:
        r = int(e[0])
        t = [int(n) for n in e[1].split(" ")]

        correct = check_equation(operations, r, t, concat, set())

        if correct:
            total += r

    return total


def check_equation(operations, r, t, concat, visited):

    op_iterations = list(itertools.product(operations, repeat=len(t) - 1))
    correct = False
    i = 0
    while not correct and i < len(op_iterations):
        concats = []
        calculation = t[0]

        if concat and len(t) > 1:
            new_concat = [int(str(calculation) + str(t[1]))] + t[2:]
            if tuple(new_concat) not in visited:
                visited.add(tuple(new_concat))
                concats.append(new_concat)

        j = 1
        for op in op_iterations[i]:
            if op == "+":
                calculation += t[j]
            elif op == "*":
                calculation *= t[j]

            if concat and j + 1 < len(t):
                new_concat = [int(str(calculation) + str(t[j+1]))] + t[j+2:]
                if tuple(new_concat) not in visited:
                    visited.add(tuple(new_concat))
                    concats.append(new_concat)

            j += 1

        if calculation == r or (len(t) == 1 and r == calculation):
            correct = True
        elif concat and len(concats) > 0:
            c = 0
            while not correct and c < len(concats):
                correct = check_equation(operations, r, concats[c], concat, visited)
                c += 1

        i += 1
    return correct


if __name__ == "__main__":
    tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

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
    p2_tst_result = solve(tst_input, True)
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p2_result = solve(puzzle_input, True)
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
