import Utils
from aocd import submit

day = 16
year = 2023
p1_expected_tst_result = 46
p2_expected_tst_result = 51

Utils.download_input(year, day)


reflections = {
    ("/", ( 0,  1)): [90],
    ("/", ( 0, -1)): [90],
    ("/", (-1,  0)): [-90],
    ("/", ( 1,  0)): [-90],

    ("\\", ( 0,  1)): [-90],
    ("\\", ( 0, -1)): [-90],
    ("\\", ( 1,  0)): [90],
    ("\\", (-1,  0)): [90],

    (".", ( 0,  1)): [0],
    (".", ( 0, -1)): [0],
    (".", ( 1,  0)): [0],
    (".", (-1,  0)): [0],

    ("-", ( 0,  1)): [0],
    ("-", ( 0, -1)): [0],
    ("-", ( 1,  0)): [-90, 90],
    ("-", (-1,  0)): [-90, 90],

    ("|", ( 0,  1)): [-90, 90],
    ("|", ( 0, -1)): [-90, 90],
    ("|", ( 1,  0)): [0],
    ("|", (-1,  0)): [0],
}


def calc_starting_points(m):
    m_x, m_y = len(m), len(m[0])
    starting_points = []

    for x in range(m_x):
        starting_points.append(((x, -1), (0, 1)))
        starting_points.append(((x, m_y), (0, -1)))

    for y in range(m_y):
        starting_points.append(((-1, y), (1, 0)))
        starting_points.append(((m_x, y), (-1, 0)))

    return starting_points

def solve(data, all = False):
    tiles = [[t for t in l] for l in data]

    max_energy_level = 0
    starting_points = calc_starting_points(tiles) if all else [((0, -1), (0, 1))]
    for starting_point in starting_points:
        work = [starting_point]
        visited = set()

        loop = True
        while loop:
            if len(work) > 0:
                visited.add(work[0])
                p, d = work.pop(0)
                n_p = p[0] + d[0], p[1] + d[1]
                if Utils.coord_valid(n_p, tiles):
                    t = Utils.at_coord(tiles, n_p)
                    work.extend([w_ for w_ in [(n_p, Utils.rotate(d, r)) for r in reflections[(t, d)]] if w_ not in work and w_ not in visited])
            else:
                loop = False

        max_energy_level = max(max_energy_level, len(set([t[0] for t in visited])) - 1)

    return max_energy_level


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
p2_tst_result = solve(tst_input, True)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    p2_result = solve(puzzle_input, True)
    submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")
