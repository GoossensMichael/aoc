import heapq
import time
import Utils
from aocd import submit

day = 16
year = 2024
p1_expected_tst_result = 11048
p2_expected_tst_result = 64

Utils.download_input(year, day)

MOVE_COST = 1
TURN_COST = 1000

def solve(m):
    s = len(m) - 2, 1
    e = 1, len(m) - 2

    pq = []
    d = (0, 1)
    heapq.heappush(pq, (0, s, d))
    tiles = {(s, d): 0}

    while pq:
        c, p, d = heapq.heappop(pq)
        for angle in [0, 90, -90]:
            n_d = d if angle == 0 else Utils.rotate(d, angle)
            cost = c + (MOVE_COST if angle == 0 else TURN_COST)
            n_p = (p[0] + n_d[0], p[1] + n_d[1]) if angle == 0 else p

            if m[n_p[0]][n_p[1]] != "#" and ((n_p, n_d) not in tiles or cost < tiles[(n_p, n_d)]):
                heapq.heappush(pq, (cost, n_p, n_d))
                tiles[(n_p, n_d)] = cost

    min_costs = min([t[1] for t in tiles.items() if t[0][0] == e])

    pq = []
    for t in tiles.items():
        if t[0][0] == e and t[1] == min_costs:
            heapq.heappush(pq, (t[1], t[0][0], t[0][1]))

    best_seats = {e}
    while pq:
        c, p, d = heapq.heappop(pq)
        for angle in [0, 90, -90]:
            n_d = d if angle == 0 else Utils.rotate(d, angle)
            n_p = p[0] - n_d[0], p[1] - n_d[1]
            cost = c - MOVE_COST - (0 if angle == 0 else TURN_COST)
            if tiles.get((n_p, n_d)) == cost:
                heapq.heappush(pq, (cost, n_p, n_d))
                best_seats.add(n_p)

    return min_costs, len(best_seats)



if __name__ == "__main__":
    tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

    print("Part 1")
    start_time = time.time()
    p1_tst_result = solve(tst_input)
    print(f"Test solution: {p1_tst_result[0]}.")
    elapsed_time = time.time() - start_time
    print(f"Time taken p1 test: {elapsed_time:.2f} seconds")
    if p1_tst_result[0] == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p1_result = solve(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p1: {elapsed_time:.2f} seconds")
        submit(p1_result[0], part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    start_time = time.time()
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p1_tst_result[1]}.")
    if p1_tst_result[1] == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p1_result[1], part="b", day=day, year=year)
    else:
        print("Test failed")
