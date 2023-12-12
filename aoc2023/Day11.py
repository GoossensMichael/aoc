import Utils
from aocd import submit

day = 11
year = 2023
p1_expected_tst_result = 374
p2_expected_tst_result = 8410

Utils.download_input(year, day)


def expand(galaxy, ):
    cols = {i: True for i in range(len(galaxy[0]))}
    for c in range(len(galaxy[0])):
        for r in galaxy:
            if r[c] != ".":
                cols[c] = False

    cols = set([j for j in cols.keys() if cols[j]])

    rows = set()
    for i, belt in enumerate(galaxy):
        c = 0
        while c < len(belt) and belt[c] == ".":
            c += 1

        if c == len(belt):
            rows.add(i)

    return (cols, rows)


def solve(data, expansion_size=2):
    expansion_size -= 1
    galaxy = [[c for c in r] for r in data]

    (cols, rows) = expand(galaxy)
    planets = [(i, j) for i, b in enumerate(galaxy) for j, p in enumerate(b) if p == "#"]

    visited_planets = []
    cnt = 0
    times = 0
    for planet in planets:
        for visited_planet in visited_planets:
            row_expansions = sum([1 for row in rows
                                  if visited_planet[0] < row < planet[0] or visited_planet[0] > row > planet[0]])
            col_expansions = sum([1 for col in cols
                                  if visited_planet[1] < col < planet[1] or visited_planet[1] > col > planet[1]])
            amt_expansions = col_expansions + row_expansions
            cnt += abs(visited_planet[0] - planet[0]) + abs(visited_planet[1] - planet[1]) + (expansion_size * amt_expansions)
            times += 1
        visited_planets.append(planet)

    print(times)

    return cnt


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
p2_tst_result = solve(tst_input, 100)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    p2_result = solve(puzzle_input, 1_000_000)
    submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")
