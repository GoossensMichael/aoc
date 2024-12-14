import math
import time
import Utils
from aocd import submit

day = 14
year = 2024
p1_expected_tst_result = 12
p2_expected_tst_result = 8053

Utils.download_input(year, day)


def parse(data):
    return [Utils.extract_int("p=%,% v=%,%", d) for d in data]


def solve(data, dur=100, dim=(101, 103)):
    robots = parse(data)

    q_h_border = int(((dim[0] - 1) / 2))
    q_v_border = int(((dim[1] - 1) / 2))

    quadrants = {"1": [], "2": [], "3": [], "4": []}
    for r in robots:
        (px, py, vx, vy) = r
        px = (px + (dur * vx)) % dim[0]
        py = (py + (dur * vy)) % dim[1]

        p = (px, py)
        q_id = None

        if q_h_border < px < dim[0] and 0 <= py < q_v_border:
            q_id = "1"
        elif 0 <= px < q_h_border and 0 <= py < q_v_border:
            q_id = "2"
        elif 0 <= px < q_h_border and q_v_border < py < dim[1]:
            q_id = "3"
        elif q_h_border < px < dim[0] and q_v_border < py < dim[1]:
            q_id = "4"

        if q_id is not None:
            quadrants[q_id].append(p)

    return math.prod([len(r) for _, r in quadrants.items()])


def display(robots, dim):
    for y in range(dim[0]):
        l = ""
        for x in range(dim[1]):
            if (x, y) in robots:
                l += "#"
            else:
                l += "."
        print(l)
    print()


def solve2(data, dim=(101, 103)):
    robots = parse(data)

    s = 0
    go = True
    while go:
        s += 1
        s_robots = []
        d_robots = set()
        lines = {}
        linesy = {}
        for r in robots:
            (px, py, vx, vy) = r
            px = (px + vx) % dim[0]
            py = (py + vy) % dim[1]

            if py not in lines:
                lines[py] = 0
            lines[py] += 1

            if px not in linesy:
                linesy[px] = 0
            linesy[px] += 1

            s_robots.append((px, py, vx, vy))
            d_robots.add((px, py))

        robots = s_robots
        if sum(1 for value in lines.values() if value > 30) > 1 and sum(1 for value in linesy.values() if value > 30) > 1:
            go = False
            display(d_robots, dim)

    return s


if __name__ == "__main__":
    tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

    print("Part 1")
    start_time = time.time()
    p1_tst_result = solve(tst_input, dim=(11, 7))
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
    p2_tst_result = solve2(puzzle_input)
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
