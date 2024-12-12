import time
import Utils
from aocd import submit

day = 12
year = 2024
p1_expected_tst_result = 1930
p2_expected_tst_result = 1206

Utils.download_input(year, day)


directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def is_in_bounds(data, x, y):
    return 0 <= x < len(data) and 0 <= y < len(data[0])


def border_count(data, i, j, t):
    c = 0
    for d in directions:
        x = i + d[0]
        y = j + d[1]
        if is_in_bounds(data, x, y):
            if data[x][y] != t:
                c += 1
        else:
            c += 1

    return c


def expand(data, i, j, t, visited):
    region = set()

    work = [(i, j)]
    region.add((i, j))

    c_b = 0
    while work:
        x, y = work.pop()
        b_c = border_count(data, x, y, t)
        c_b += b_c

        for d_x, d_y in directions:
            n_x, n_y = x + d_x, y + d_y
            if is_in_bounds(data, n_x, n_y) and data[n_x][n_y] == t and (n_x, n_y) not in region:
                work.append((n_x, n_y))
                region.add((n_x, n_y))

        visited.add((x, y))

    return len(region) * c_b


def solve(data):
    visited = set()

    total = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if (i, j) not in visited:
                t = data[i][j]
                total += expand(data, i, j, t, visited)

    return total


def collect_borders(data, i, j, t, bounds):
    for d in directions:
        x = i + d[0]
        y = j + d[1]

        outside = False
        if is_in_bounds(data, x, y):
            if data[x][y] != t:
                outside = True
        else:
            outside = True

        if outside:
            if d[0] != 0:
                direction = "H"
                leading_coord = x
                other_coord = y
                origin = i
            else:
                direction = "V"
                leading_coord = y
                other_coord = x
                origin = j

            if leading_coord not in bounds[direction]:
                bounds[direction][leading_coord] = {}
            if origin not in bounds[direction][leading_coord]:
                bounds[direction][leading_coord][origin] = []
            bounds[direction][leading_coord][origin].append(other_coord)


def count_borders(bounds):
    cnt = 0

    for direction, coords in bounds.items():
        for _, origins in coords.items():
            for _, other_coords in origins.items():
                sorted_other_coords = sorted(other_coords)

                cnt += 1
                c = sorted_other_coords.pop(0)
                while sorted_other_coords:
                    n = sorted_other_coords.pop(0)
                    if c + 1 != n:
                        cnt += 1
                    c = n

    return cnt


def expand2(data, i, j, t, visited):
    region = set()
    bounds = {"H": {}, "V": {}}

    work = [(i, j)]
    region.add((i, j))

    while work:
        x, y = work.pop()
        collect_borders(data, x, y, t, bounds)

        for d_x, d_y in directions:
            n_x, n_y = x + d_x, y + d_y
            if is_in_bounds(data, n_x, n_y) and data[n_x][n_y] == t and (n_x, n_y) not in region:
                work.append((n_x, n_y))
                region.add((n_x, n_y))

        visited.add((x, y))

    borders = count_borders(bounds)
    return len(region) * borders


def solve2(data):
    visited = set()

    total = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            if (i, j) not in visited:
                t = data[i][j]
                total += expand2(data, i, j, t, visited)

    return total


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
