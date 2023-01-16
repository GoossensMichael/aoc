import Utils

day = 0

def solve(data):
    return 0


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_test = solve(tst_input)
print(f"Test solution: {p1_test}.")
if p1_test == 330:
    p1 = solve(puzzle_input)
    print(f"Puzzle solution: {p1}.")

print()
print("Part 2")
p2_test = solve(tst_input)
print(f"Test solution: {p2_test}.")
if p2_test == -1:
    print(f"Puzzle solution: {solve(puzzle_input)}.")
