import Utils
from aocd import submit

day = 18
year = 2023
p1_expected_tst_result = 62
p2_expected_tst_result = 952408144115

Utils.download_input(year, day)

directions = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}
dir_corrections = {"0": "R", "1": "D", "2": "L", "3": "U"}


def correct(instructions):
    return [(dir_corrections[c[-1]], int(c[:5], 16), c) for _, _, c in instructions]


def solve(data, faulty_instructions = False):
    instructions = [(d, int(s), c) for d, s, c in [Utils.extract_string("% % (#%)", l) for l in data]]

    if faulty_instructions:
        instructions = correct(instructions)

    x_ranges = {}
    y_ranges = []
    location = (0, 0)
    for d, s, _ in instructions:
        if d in ["U", "D"]:
            x1 = location[0]
            x2 = location[0] + (s * directions[d][0])
            y_ranges.append((location[1], (min(x1, x2), max(x1, x2))))
            location = (x2, location[1])
        else:
            if location[0] not in x_ranges:
                x_ranges[location[0]] = []
            y1 = location[1]
            y2 = location[1] + (s * directions[d][1])
            x_ranges[location[0]].append((min(y1, y2), max(y1, y2)))
            location = (location[0], y2)

    y_ranges.sort()
    cnt = 0
    while len(y_ranges) > 0:
        y_range = y_ranges.pop(0)
        o_idx = first_overlap_index(y_range, y_ranges)
        if o_idx is None:
            y_ranges = []
            continue
        o_range = y_ranges.pop(o_idx)

        x_min = max(y_range[1][0], o_range[1][0])
        x_max = min(y_range[1][1], o_range[1][1])
        cnt += (o_range[0] - y_range[0] + 1) * (x_max - x_min + 1)

        if x_min in x_ranges:
            x_ranges[x_min] = reduce_x_ranges(x_ranges[x_min], y_range[0], o_range[0])
        if x_max in x_ranges:
            x_ranges[x_max] = reduce_x_ranges(x_ranges[x_max], y_range[0], o_range[0])

        if y_range[1] != o_range[1]:
            if y_range[1][0] < o_range[1][0] - 1:
                y_ranges.append((y_range[0], (y_range[1][0], o_range[1][0] - 1)))
            if y_range[1][1] > o_range[1][1] + 1:
                y_ranges.append((y_range[0], (o_range[1][1] + 1, y_range[1][1])))
            if o_range[1][0] < y_range[1][0] - 1:
                y_ranges.append((o_range[0], (o_range[1][0], y_range[1][0] - 1)))
            if o_range[1][1] > y_range[1][1] + 1:
                y_ranges.append((o_range[0], (y_range[1][1] + 1, o_range[1][1])))

        y_ranges = filter_small_overlap(x_min, x_max, y_range[0], o_range[0], y_ranges)

    for x_ranges_ in x_ranges.values():
        for x_range in x_ranges_:
            cnt += x_range[1] - x_range[0] + 1

    return cnt


def reduce_x_ranges(x_ranges, min_y, max_y):
    n_x_ranges = []
    for x_range in x_ranges:
        if not (min_y <= x_range[0] <= x_range[1] <= max_y):
            if x_range[0] == min_y:
                x_0 = min_y + 1
            elif x_range[0] == max_y:
                x_0 = max_y + 1
            else:
                x_0 = x_range[0]

            if x_range[1] == min_y:
                x_1 = min_y - 1
            elif x_range[1] == max_y:
                x_1 = max_y - 1
            else:
                x_1 = x_range[1]

            n_x_ranges.append((x_0, x_1))

    return n_x_ranges


def filter_small_overlap(x_min, x_max, y_min, y_max, y_ranges):
    n_y_ranges = []

    for y_range in y_ranges:
        if y_min < y_range[0] < y_max:
            if y_range[1][0] == x_max:
                n_y_ranges.append((y_range[0], (y_range[1][0] + 1, y_range[1][1])))
            elif y_range[1][1] == x_min:
                n_y_ranges.append((y_range[0], (y_range[1][0], y_range[1][1] - 1)))
            else:
                n_y_ranges.append(y_range)
        else:
            n_y_ranges.append(y_range)

    n_y_ranges.sort()

    return n_y_ranges


def first_overlap_index(r1, ranges):
    for i, r2 in enumerate(ranges):
        if r2[0] > r1[0] and r2[1][1] > r1[1][0] and r2[1][0] < r1[1][1]:
            return i
    return None


def print_hole(m, min_x, max_x, min_y, max_y):
    for i in range(min_x, max_x + 1):
        for j in range(min_y, max_y + 1):
            if (i, j) in m:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


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
