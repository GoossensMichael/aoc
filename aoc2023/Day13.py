import Utils
from aocd import submit

day = 13
year = 2023
p1_expected_tst_result = 405
p2_expected_tst_result = 400

Utils.download_input(year, day)


def verify(terrain, i, smudge, not_one_diff_joker_used):
    if smudge:
        one_diff_joker = not_one_diff_joker_used
        for j in range(1, min(i + 1, len(terrain) - i - 1)):
            if terrain[i - j] != terrain[i + j + 1]:
                if one_diff_joker and one_difference(terrain[i - j], terrain[i + j + 1]):
                    one_diff_joker = False
                else:
                    return False
        return not one_diff_joker

    else:
        for j in range(1, min(i + 1, len(terrain) - i - 1)):
            if terrain[i - j] != terrain[i + j + 1]:
                return False
        return True


def one_difference(x, y):
    return 1 == sum([1 for i, x_ in enumerate(x) if x_ != y[i]])



def summarize(terrain, multiplier = 1, smudge = False):
    i = 0
    while i < len(terrain) - 1:
        if smudge:
            one_diff_joker_used = one_difference(terrain[i], terrain[i + 1])
        else:
            one_diff_joker_used = False
        if terrain[i] == terrain[i + 1] or one_diff_joker_used:
            if verify(terrain, i, smudge, not one_diff_joker_used):
                return multiplier * (i + 1)
        i += 1
    return 0


def transpose(terrain):
    t = []
    for i in range(len(terrain)):
        for j in range(len(terrain[i])):
            if len(t) - 1 < j:
                t.append("")
            t[j] += terrain[i][j]

    return t


def solve(data, smudge = False):
    terrains = data.split("\n\n")

    return sum([summarize([ts for ts in t.split("\n") if ts != ""], 100, smudge) + summarize(transpose([ts for ts in t.split("\n") if ts != ""]), 1, smudge) for t in terrains])


tst_input = Utils.read_input_flat(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input_flat(f"input/day{day}_input.txt")

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
