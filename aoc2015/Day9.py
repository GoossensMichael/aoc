import Utils

template = "% to % = %"


def parseInput(lines):
    routes = {}
    destinations = set()
    for line in lines:
        f, t, d = Utils.extract_string(template, line)
        routes[(f, t)] = int(d)
        destinations.add(f)
        destinations.add(t)

    return (routes, destinations)


def solve(lines):
    routes, destinations = parseInput(lines)


tst_input = Utils.read_input("input/day9_tst_input.txt")
puzzle_input = Utils.read_input("input/day9_input.txt")

print("Part 1")
print(f"Test input: {solve(tst_input)}.")
print(f"Puzzle input: {solve(puzzle_input)}.")

print()
print("Part 2")
print(f"Test input: {solve(tst_input)}.")
print(f"Puzzle input: {solve(puzzle_input)}.")
