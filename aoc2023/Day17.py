from queue import PriorityQueue

import Utils
from aocd import submit

day = 17
year = 2023
p1_expected_tst_result = 102
p2_expected_tst_result = 94

Utils.download_input(year, day)


def search(m, min_blocks, max_blocks):
    m_x = len(m) - 1
    m_y = len(m[0]) - 1

    q = PriorityQueue()
    q.put((0, (0, 0), ((0, 1), 0)))
    visited = {((0, 0), ((0, 1), 0))}

    result = None
    while result is None:
        temp, pos, prev_direction = q.get()

        for deg in [-90, 0, 90]:
            new_direction = determine_new_direction(deg, max_blocks, min_blocks, prev_direction)
            if new_direction:
                new_pos = Utils.add_2d(pos, new_direction[0])
                if Utils.coord_valid(new_pos, m) and ((new_pos, new_direction) not in visited):
                    new_temp = temp + m[new_pos[0]][new_pos[1]]
                    if new_pos == (m_x, m_y) and result is None:
                        result = new_temp

                    visited.add((new_pos, new_direction))
                    q.put((new_temp, new_pos, new_direction))

    return result


def determine_new_direction(deg, max_dir_length, min_dir_length, prev_direction):
    if deg == 0 and prev_direction[1] != max_dir_length:
        new_direction = ((prev_direction[0][0], prev_direction[0][1]), prev_direction[1] + 1)
    elif deg != 0 and prev_direction[1] >= min_dir_length:
        new_direction = (Utils.rotate(prev_direction[0], deg), 1)
    else:
        new_direction = None

    return new_direction


def solve(data):
    m = Utils.tiles_int(data)

    return search(m,0, 3), search(m, 4, 10)


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input)[0]
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    print("Test passed - Calculating real input now")
    p1_result = solve(puzzle_input)[0]
    submit(p1_result, part="a", day=day, year=year)
else:
    print("Test failed")

print()
print("Part 2")
p2_tst_result = solve(tst_input)[1]
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    p2_result = solve(puzzle_input)[1]
    submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")
