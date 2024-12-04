import Utils
from aocd import submit
import numpy as np

day = 1
year = 2024
p1_expected_tst_result = 11
p2_expected_tst_result = 31

Utils.download_input(year, day)

def solve(data):

    # Initialize the lists
    list1 = []
    list2 = []

    # Process each line in the data
    for row in data:
        # Split the row into two numbers by whitespace
        num1, num2 = map(int, row.split())
        # Append numbers to respective lists
        list1.append(num1)
        list2.append(num2)

    # Sort both columns
    sorted_col1 = np.sort(list1)
    sorted_col2 = np.sort(list2)

    # Calculate absolute differences and sum them
    absolute_differences = np.abs(sorted_col1 - sorted_col2)
    total_difference = np.sum(absolute_differences)

    # Initialize the similarity score
    similarity_score = 0

    # Calculate the similarity score
    for num in sorted_col1:
        # Count how many times `num` appears in the right list
        count = sum(1 for x in sorted_col2 if x == num)
        # Add to the similarity score
        similarity_score += num * count

    return total_difference, similarity_score

if __name__ == "__main__":
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
