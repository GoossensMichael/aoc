import time
import Utils
from aocd import submit

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

day = 20
year = 2024
p1_expected_tst_result = 10
p2_expected_tst_result = 41

Utils.download_input(year, day)


def parse(data):
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == "S":
                s = (i, j)
            elif data[i][j] == "E":
                e = (i, j)

    return s, e



def get_cheat_permutations(cheat):
    cheats = set()
    for i in range(-cheat, cheat + 1):
        for j in range(0, cheat - abs(i) + 1):
            if (abs(i) + abs(j)) > 1:
                cheats.add((i, j))
                cheats.add((i, -j))

    return cheats

Utils.print_map_points(get_cheat_permutations(2))
Utils.print_map_points(get_cheat_permutations(3))
Utils.print_map_points(get_cheat_permutations(4))
Utils.print_map_points(get_cheat_permutations(5))
Utils.print_map_points(get_cheat_permutations(20))


def solve(data, th = 10, cheat_duration=2):
    s, e = parse(data)

    x, y = s
    m = {(x, y): 0}
    m_a = {}
    while (x, y) != e:
        for d in DIRECTIONS:
            x_n = x + d[0]
            y_n = y + d[1]

            if data[x_n][y_n] in ("E", ".") and (x_n, y_n) not in m:
                break

        m[(x_n, y_n)] = m[(x, y)] + 1
        x = x_n
        y = y_n

    cnt = 0
    for x, y in m:
        cheats = get_cheat_permutations(cheat_duration)
        for c in cheats:
            x_a = x + c[0]
            y_a = y + c[1]
            c_d = abs(c[0]) + abs(c[1])
            if 0 <= x_a < len(data) and 0 <= y_a < len(data[0]) and data[x_a][y_a] in ("E", "."):
                if m[(x_a, y_a)] > m[(x, y)] + c_d:
                    if (x_a, y_a) not in m_a:
                        m_a[(x_a, y_a)] = []
                    m_a[(x_a, y_a)].append((x_a, y_a))

                    gain = m[(x_a, y_a)] - (m[(x, y)] + c_d)
                    cnt += 1 if gain >= th else 0

    return cnt


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
        p1_result = solve(puzzle_input, 100)
        elapsed_time = time.time() - start_time
        print(f"Time taken p1: {elapsed_time:.2f} seconds")
        submit(p1_result, part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    start_time = time.time()
    p2_tst_result = solve(tst_input, 70, 20)
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p2_result = solve(puzzle_input, 100, 20)
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
