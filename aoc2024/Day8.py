import time
import Utils
from aocd import submit

day = 8
year = 2024
p1_expected_tst_result = 14
p2_expected_tst_result = 34

Utils.download_input(year, day)


def parse(data):
    antennas_by_id = {}

    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] != ".":
                id = data[i][j]
                if id not in antennas_by_id.keys():
                    antennas_by_id[id] = []
                antennas_by_id[id].append((i, j))

    return antennas_by_id


def solve(data):
    antennas_by_id = parse(data)
    max_r = len(data)
    max_c = len(data[0])

    anti_nodes = set()
    for id in antennas_by_id.keys():
        antennas = antennas_by_id[id]
        for l in range(len(antennas)):
            a = antennas[l]
            for o_l in range(l + 1, len(antennas)):
                b = antennas[o_l]

                d = (b[0] - a[0], b[1] - a[1])

                for f in [2, -1]:
                    p = (a[0] + (d[0] * f), a[1] + (d[1] * f))

                    if 0 <= p[0] < max_r and 0 <= p[1] < max_c:
                        anti_nodes.add(p)

    return len(anti_nodes)


def solve2(data):
    antennas_by_id = parse(data)
    max_r = len(data)
    max_c = len(data[0])

    anti_nodes = set()
    for id in antennas_by_id.keys():
        antennas = antennas_by_id[id]
        for l in range(len(antennas)):
            a = antennas[l]
            for o_l in range(l + 1, len(antennas)):
                b = antennas[o_l]

                d = (b[0] - a[0], b[1] - a[1])

                for f in [1, -1]:
                    p = a
                    i = 1
                    while 0 <= p[0] < max_r and 0 <= p[1] < max_c:
                        anti_nodes.add(p)

                        p = (a[0] + (d[0] * f * i), a[1] + (d[1] * f * i))
                        i += 1

    return len(anti_nodes)


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
