import Utils

day = 3


def parse_p1(data):
    result = []
    for triangle in data:
        (a, b, c) = triangle.strip().split()
        result.append((int(a), int(b), int(c)))

    return result


def parse_p2(data):
    cols = [[], [], []]
    for triple in data:
        (a, b, c) = triple.strip().split()
        cols[0].append(int(a))
        cols[1].append(int(b))
        cols[2].append(int(c))

    seq = cols[0] + cols[1] + cols[2]

    result = []
    i = 0
    while i < len(seq) - 2:
        result.append((seq[i], seq[i + 1], seq[i + 2]))
        i += 3

    return result


def solve(data, parse):
    triangles = parse(data)

    valid_triangles = 0
    for (a, b, c) in triangles:
        if a + b > c and a + c > b and b + c > a:
            valid_triangles += 1

    return valid_triangles


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_test = solve(tst_input, parse_p1)
print(f"Test solution: {p1_test}.")
if p1_test == 2:
    p1 = solve(puzzle_input, parse_p1)
    print(f"Puzzle solution: {p1}.")

print()
print("Part 2")
p2_test = solve(tst_input, parse_p2)
print(f"Test solution: {p2_test}.")
if p2_test == 3:
    print(f"Puzzle solution: {solve(puzzle_input, parse_p2)}.")
