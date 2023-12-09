import Utils
from aocd import submit

day = 9
year = 2023
p1_expected_tst_result = 114
p2_expected_tst_result = 2

Utils.download_input(year, day)


def extrapolate(d):
    seq = [[int(n) for n in d.split()]]
    while sum([1 for n in seq[-1] if n != 0]) > 0:
        seq.append([seq[-1][i] - seq[-1][i - 1] for i in range(1, len(seq[-1]))])

    predict_next = 0
    for extrapolation in seq[::-1]:
        predict_next = predict_next + extrapolation[-1]

    predict_previous = 0
    for extrapolation in seq[::-1]:
        predict_previous = extrapolation[0] - predict_previous

    return predict_previous, predict_next


def solve(data, i=1):
    return sum([p[i] for p in [extrapolate(d) for d in data]])


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
p2_tst_result = solve(tst_input, 0)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    p2_result = solve(puzzle_input, 0)
    submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")
