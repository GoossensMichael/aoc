import Utils
from aocd import submit

day = 14
year = 2023
p1_expected_tst_result = 136
p2_expected_tst_result = 64

Utils.download_input(year, day)


def is_valid_coord(m, c):
    return 0 <= c[0] < len(m) and 0 <= c[1] < len(m[0])


def apply_gravity(m, c, d):
    loop = True
    n_c = (c[0], c[1])

    while loop:
        p_c = (n_c[0] + d[0], n_c[1] + d[1])
        if is_valid_coord(m, p_c) and m[p_c[0]][p_c[1]] == ".":
            n_c = p_c
        else:
            loop = False

    return n_c


def solve(data, cycles = 1, cycle = tuple([(-1, 0)])):
    m = [[rock for rock in l] for l in data]

    hash_map = {}
    i = 0
    pattern_not_found = True
    while i < cycles:
        i += 1
        for d in cycle:
            for x in range(len(m)) if d[0] < 0 else reversed(range(len(m))):
                for y in range(len(m[0])) if d[1] < 0 else  reversed(range(len(m[0]))):
                    if m[x][y] == "O":
                        n_c = apply_gravity(m, (x, y), d)
                        m[x][y] = "."
                        m[n_c[0]][n_c[1]] = "O"

        hash = ''.join([''.join(row) for row in m])
        if pattern_not_found:
            if hash in hash_map:
                pattern_not_found = False
                repeat_length = i - hash_map[hash]
                i = cycles - ((cycles - i) % repeat_length)
            else:
                hash_map[hash] = i

    total = 0
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j] == "O":
                total += len(m) - i

    return total


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    print("Test passed - Calculating real input now")
    p1_result = solve(puzzle_input)
    submit(p1_result, part="a", day=day, year=year)
else:
    print("Test failed")

print()
print("Part 2")
p2_tst_result = solve(tst_input, 1_000_000_000, [(-1, 0), (0, -1), (1, 0), (0, 1)])
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    p2_result = solve(puzzle_input, 1_000_000_000, [(-1, 0), (0, -1), (1, 0), (0, 1)])
    submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")
