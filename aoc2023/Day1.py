import Utils
from aocd import submit

day = 1
year = 2023
p1_expected_tst_result = 142
p2_expected_tst_result = 281

Utils.download_input(year, day)

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
numbers_r = [n[::-1] for n in numbers]

def number_starts_here(txt, number):
    return txt[:len(number)] == number

def findFirstDigit(txt, scan, numbers):
    if (not scan):
        for i in txt:
            if i.isdigit():
                return i
    else:
        for i, char in enumerate(txt):
            if char.isdigit() or any(txt[i:].startswith(num) for num in numbers):
                return char if char.isdigit() else numbers.index(next(num for num in numbers if txt[i:].startswith(num))) + 1


def solve(data, scan=False):
    return sum(int(str(findFirstDigit(i, scan, numbers)) + str(findFirstDigit(i[::-1], scan, numbers_r))) for i in data)

tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    p1_result = solve(puzzle_input)
    print(f"Puzzle solution: {p1_result}.")
    if (input("submit part 1? (y or n) - ") == "y"):
        submit(p1_result, part="a", day=day, year=year)

tst_input = Utils.read_input(f"input/day{day}_tst2_input.txt")

print()
print("Part 2")
p2_tst_result = solve(tst_input, True)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    p2_result = solve(puzzle_input, True)
    print(f"Puzzle solution: {p2_result}.")
    if (input("submit part 2? (y or n) - ") == "y"):
        submit(p2_result, part="b", day=day, year=year)
