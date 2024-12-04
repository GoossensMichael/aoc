import Utils
from aocd import submit
import re

day = 3
year = 2024
p1_expected_tst_result = 161
p2_expected_tst_result = 48

Utils.download_input(year, day)


def solve(data):
    pattern = r"mul\(\d+,\d+\)"
    matches = re.findall(pattern, data)

    multiplications = [Utils.extract_int("mul(%,%)", m) for m in matches]
    result = sum([m[0] * m[1] for m in multiplications])

    return result

def solve2(data):
    pattern = r"do\(\)|don't\(\)|mul\(\d+,\d+\)"

    matches = re.findall(pattern, data)

    execute = True
    result = 0
    for s in matches:
        if s == "don't()":
            execute = False
        elif s == "do()":
            execute = True
        elif execute:
            numbers = Utils.extract_int("mul(%,%)", s)
            result = result + (numbers[0] * numbers[1])

    return result


if __name__ == "__main__":
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
    tst2_input = Utils.read_input_flat(f"input/day{day}_tst2_input.txt")
    p2_tst_result = solve2(tst2_input)
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        p2_result = solve2(puzzle_input)
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
