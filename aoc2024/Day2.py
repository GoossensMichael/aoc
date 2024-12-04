import Utils
from aocd import submit

day = 2
year = 2024
p1_expected_tst_result = 2
p2_expected_tst_result = 4

Utils.download_input(year, day)

def is_valid_row(row):
    # Determine the direction of the first step
    direction = None  # 'increasing' or 'decreasing'

    for i in range(len(row) - 1):
        diff = row[i + 1] - row[i]
        if abs(diff) < 1 or abs(diff) > 3:  # Check the step size
            return False
        if direction is None:  # Establish the direction
            direction = 'increasing' if diff > 0 else 'decreasing'
        elif direction == 'increasing' and diff <= 0:  # Breaks increasing rule
            return False
        elif direction == 'decreasing' and diff >= 0:  # Breaks decreasing rule
            return False

    return True

def count_valid_rows(matrix):
    count = 0
    for row in matrix:
        if is_valid_row(row):
            count += 1
    return count

def is_valid_row_with_tolerance(row):
    direction = None  # 'increasing' or 'decreasing'

    for i in range(len(row) - 1):
        diff = row[i + 1] - row[i]

        if abs(diff) < 1 or abs(diff) > 3:  # Invalid step size
            return is_valid_after_removal_of_error(i, row)
        else:
            if direction is None:  # Establish the direction
                direction = 'increasing' if diff > 0 else 'decreasing'
            elif direction == 'increasing' and diff <= 0:  # Breaks increasing rule
                return is_valid_after_removal_of_error(i, row)
            elif direction == 'decreasing' and diff >= 0:  # Breaks decreasing rule
                return is_valid_after_removal_of_error(i, row)

    return True


def is_valid_after_removal_of_error(i, row):
    return is_valid_row(row[:i] + row[i + 1:]) or is_valid_row(row[:i + 1] + row[i + 2:]) or is_valid_row(row[1:])


def count_valid_rows_with_tolerance(matrix):
    count = 0
    for row in matrix:
        if is_valid_row_with_tolerance(row):
            count += 1
    return count

def parse(data):
    matrix = []
    for line in data:
        row = list(map(int, line.split()))  # Convert space-separated values to integers
        matrix.append(row)

    return matrix

def solve(data):
    return count_valid_rows(parse(data))

def solve2(data):
    return count_valid_rows_with_tolerance(parse(data))

if __name__ == "__main__":
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
    p2_tst_result = solve2(tst_input)
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        p2_result = solve2(puzzle_input)
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
