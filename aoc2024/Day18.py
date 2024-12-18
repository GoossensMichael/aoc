import heapq
import time
import Utils
from aocd import submit

day = 18
year = 2024
p1_expected_tst_result = 22
p2_expected_tst_result = "6,1"

Utils.download_input(year, day)


def solve(data, dimensions=(70, 70), kb_limit=1024):
    dim_x, dim_y = dimensions
    _bytes = set([(int(y), int(x)) for x, y in [d.split(",") for d in data[:(min(len(data), kb_limit))]]][0:kb_limit])

    memory = {(0, 0): 0}
    pq = []
    heapq.heappush(pq, (0, (0, 0)))
    while pq:
        w, p = heapq.heappop(pq)
        for d in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = p[0] + d[0], p[1] + d[1]
            if 0 <= x <= dim_x and 0 <= y <= dim_y and (x, y) not in _bytes and ((x, y) not in memory or memory[(x, y)] > w + 1):
                memory[(x, y)] = w + 1
                heapq.heappush(pq, (w + 1, (x, y)))

    return memory


def solve1(data, dimensions=(70, 70), kb_limit=1024):
    solution = solve(data, dimensions, kb_limit)
    return solution[(dimensions[0], dimensions[1])]


def solve2(data, dimensions=(70, 70), kb_limit=1024):
    search = True
    while search:
        kb_limit += 1
        solution = solve(data, dimensions, kb_limit)
        if (dimensions[0], dimensions[1]) not in solution:
            search = False

    return f"{data[kb_limit - 1]}"


if __name__ == "__main__":
    tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

    print("Part 1")
    start_time = time.time()
    p1_tst_result = solve1(tst_input, (6, 6), 12)
    print(f"Test solution: {p1_tst_result}.")
    elapsed_time = time.time() - start_time
    print(f"Time taken p1 test: {elapsed_time:.2f} seconds")
    if p1_tst_result == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p1_result = solve1(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p1: {elapsed_time:.2f} seconds")
        submit(p1_result, part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    start_time = time.time()
    p2_tst_result = solve2(tst_input, (6, 6), 12)
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
