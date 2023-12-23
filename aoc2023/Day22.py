from queue import PriorityQueue

from aocd import submit

import Utils

day = 22
year = 2023
p1_expected_tst_result = 5
p2_expected_tst_result = 7

Utils.download_input(year, day)


class Brick:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.floor = min(self.start[2], self.end[2])
        self.height = abs(self.start[2] - self.end[2])
        self.support = []
        self.supporting = []

    def __lt__(self, other):
        return self.floor < other.floor


def parse(data):
    bricks = PriorityQueue()
    lowest_level = None
    for l, r in [d.split("~") for d in data]:
        brick = Brick([int(v) for v in l.split(",")], [int(v) for v in r.split(",")])
        bricks.put(brick)
        if lowest_level is None or lowest_level > brick.floor:
            lowest_level = brick.floor
    return bricks, lowest_level


def solve(data):
    bricks, floor_level = parse(data)

    stable_bricks = []
    while not bricks.empty():
        brick = bricks.get()
        if brick.floor == floor_level:
            stable_bricks.append(brick)
        else:
            support, support_level = [], 0
            for stable_brick in stable_bricks:
                if stable_brick.start[0] <= brick.end[0] and brick.start[0] <= stable_brick.end[0] and\
                   stable_brick.start[1] <= brick.end[1] and brick.start[1] <= stable_brick.end[1]:
                    stable_brick_top = stable_brick.floor + stable_brick.height
                    if stable_brick_top > support_level: support, support_level = [], stable_brick_top
                    if stable_brick_top == support_level: support.append(stable_brick)
            brick.support = support
            brick.floor = support_level + 1
            stable_bricks.append(brick)

            for s_brick in support:
                s_brick.supporting.append(brick)

    cnt_p1 = 0
    for stable_brick in stable_bricks:
        if len(stable_brick.supporting) > 0:
            if sum([1 for s in stable_brick.supporting if len(s.support) > 1]) == len(stable_brick.supporting):
                cnt_p1 += 1
        else:
            cnt_p1 += 1

    cnt_p2 = 0
    for stable_brick in stable_bricks:
        fall_stack = [s for s in stable_brick.supporting if len(s.support) == 1]
        fallen = set()
        while len(fall_stack) > 0:
            falling_brick = fall_stack.pop(0)
            fallen.add(falling_brick)
            fall_stack.extend([s for s in falling_brick.supporting if len(set(s.support).difference(fallen)) == 0])
        cnt_p2 += len(fallen)

    return cnt_p1, cnt_p2


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result[0]}.")
if p1_tst_result[0] == p1_expected_tst_result:
    print("Test passed - Calculating real input now")
    p1_result = solve(puzzle_input)
    submit(p1_result[0], part="a", day=day, year=year)
else:
    print("Test failed")

print()
print("Part 2")
print(f"Test solution: {p1_tst_result[1]}.")
if p1_tst_result[1] == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    submit(p1_result[1], part="b", day=day, year=year)
else:
    print("Test failed")
