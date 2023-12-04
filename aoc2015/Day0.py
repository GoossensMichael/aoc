import Utils
from aocd import submit

day = 0
year = 2023
p1_expected_tst_result = 0
p2_expected_tst_result = 0

Utils.download_input(year, day)

def solve(data):
    return 0

tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    p1_result = solve(puzzle_input)
    print(f"Puzzle solution: {p1_result}.")
    if input("submit part 1? (y or n) - ") == "y":
        submit(p1_result, part="a", day=day, year=year)

print()
print("Part 2")
p2_tst_result = solve(tst_input)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    p2_result = solve(puzzle_input)
    print(f"Puzzle solution: {p2_result}.")
    if input("submit part 2? (y or n) - ") == "y":
        submit(p2_result, part="b", day=day, year=year)
