import time
import Utils
from aocd import submit

day = 10
year = 2024
p1_expected_tst_result = 36
p2_expected_tst_result = 81

Utils.download_input(year, day)


dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def solve(data):
    paths = set([(int(value), i, j, i, j) for i, row in enumerate(data) for j, value in enumerate(row) if value == '0'])

    count = 0
    visited = paths.copy()
    while paths:
        v, x, y, o_x, o_y = paths.pop()

        if v == 9:
            count += 1
        else:
            for d in dirs:
                x_n = x + d[0]
                y_n = y + d[1]
                if 0 <= x_n < len(data) and 0 <= y_n < len(data[x]) and int(data[x_n][y_n]) == v + 1:
                    n_p = (v + 1, x_n, y_n, o_x, o_y)
                    if n_p not in visited:
                        visited.add(n_p)
                        paths.add(n_p)

    return count


def solve2(data):
    paths = [(int(value), i, j) for i, row in enumerate(data) for j, value in enumerate(row) if value == '0']

    count = 0
    while paths:
        v, x, y = paths.pop()

        if v == 9:
            count += 1
        else:
            for d in dirs:
                x_n = x + d[0]
                y_n = y + d[1]
                if 0 <= x_n < len(data) and 0 <= y_n < len(data[x]) and int(data[x_n][y_n]) == v + 1:
                    paths.append((v + 1, x_n, y_n))

    return count


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
    p2_tst_result = solve2(tst_input)
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p2_result = solve2(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
