from aocd import submit

import Utils

day = 15
year = 2023
p1_expected_tst_result = 1320
p2_expected_tst_result = 145

Utils.download_input(year, day)


def hash(step):
    h = 0
    for c in step:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def add_or_replace_lens(boxes, step):
    (label, focal_length) = Utils.extract_string("%=%", step)
    box_number = hash(label)
    focal_length = int(focal_length)
    if box_number not in boxes:
        boxes[box_number] = {"labels": [], "focal_lengths": []}
    box = boxes[box_number]
    if label in box["labels"]:
        index = box["labels"].index(label)
        box["focal_lengths"][index] = focal_length
    else:
        box["labels"].append(label)
        box["focal_lengths"].append(focal_length)


def remove_lens(boxes, step):
    label = step[:-1]
    box_number = hash(label)
    if box_number in boxes and label in boxes[box_number]["labels"]:
        index = boxes[box_number]["labels"].index(label)
        del boxes[box_number]["labels"][index]
        del boxes[box_number]["focal_lengths"][index]


def solve(data):
    steps = data[0].split(",")

    boxes = {}
    for step in steps:
        if step[-1] == "-":
            remove_lens(boxes, step)
        elif "=" in step:
            add_or_replace_lens(boxes, step)

    return sum([hash(step) for step in steps]), sum((box_number + 1) * (slot + 1) * focal_length
                                                    for box_number, box_content in boxes.items()
                                                    for slot, focal_length in enumerate(box_content["focal_lengths"]))


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result, _ = solve(tst_input)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    print("Test passed - Calculating real input now")
    p1_result, _ = solve(puzzle_input)
    submit(p1_result, part="a", day=day, year=year)
else:
    print("Test failed")

print()
print("Part 2")
_, p2_tst_result = solve(tst_input)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    _, p2_result = solve(puzzle_input)
    submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")
