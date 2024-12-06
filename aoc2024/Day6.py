import time

import Utils
from aocd import submit

day = 6
year = 2024
p1_expected_tst_result = 41
p2_expected_tst_result = 6

Utils.download_input(year, day)


def rotate(dir):
    return dir[1], -dir[0]


def determine_position(map):
    for i in range(0, len(map)):
        for j in range(0, len(map[i])):
            if map[i][j] == "^":
                return i, j

    raise ValueError("No guard found.")


def is_within_bound(pos, map):
    return 0 <= pos[0] < len(map) and 0 <= pos[1] < len(map[0])


def solve(m):
    d = (-1, 0)
    p = determine_position(m)

    visited = set()
    visited.add(p)

    while is_within_bound(p, m):
        step_taken = False
        while not step_taken:
            n_p = tuple(a + b for a, b in zip(p, d))
            if 0 <= n_p[0] < len(m) and 0 <= n_p[1] < len(m[0]) and m[n_p[0]][n_p[1]] == "#":
                d = rotate(d)
            else:
                p = n_p
                visited.add(p)
                step_taken = True

    return len(visited) - 1, visited


def can_place_obstruction(p, m):
    return m[p[0]][p[1]] == "."


def solve2(m, visited):
    i_d = (-1, 0)
    i_p = determine_position(m)

    loops = 0
    # Improvement that I didn't make. Actually the object should only be placed on locations that could be
    # visited in the solution of part 1.
    for i, j in visited:
        if is_within_bound((i, j), m):
            m[i] = m[i][0:j] + "#" + m[i][j + 1:]
            d = i_d
            p = i_p
            visited = set()
            visited.add((i_p, i_d))

            loop = False
            while not loop and is_within_bound(p, m):
                step_taken = False
                while not step_taken:
                    n_p = tuple(a + b for a, b in zip(p, d))
                    if 0 <= n_p[0] < len(m) and 0 <= n_p[1] < len(m[0]) and m[n_p[0]][n_p[1]] == "#":
                        d = rotate(d)
                    else:
                        p = n_p
                        if (p, d) in visited:
                            loop = True
                            loops += 1
                        else:
                            visited.add((p, d))
                        step_taken = True

            m[i] = m[i][0:j] + "." + m[i][j + 1:]

    return loops


if __name__ == "__main__":
    tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

    print("Part 1")
    start_time = time.time()
    p1_tst_result = solve(tst_input)
    elapsed_time = time.time() - start_time
    print(f"Time taken p1 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p1_tst_result}.")
    if p1_tst_result[0] == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p1_result= solve(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p1: {elapsed_time:.2f} seconds")
        submit(p1_result[0], part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    start_time = time.time()
    p2_tst_result = solve2(tst_input, p1_tst_result[1])
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p2_result = solve2(puzzle_input, p1_result[1])
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
