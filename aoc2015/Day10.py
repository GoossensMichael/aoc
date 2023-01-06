def occurs(data, c):
    i = 0
    while i < len(data) and data[i] == c:
        i += 1

    return i


def split(data):
    lst = []

    i = 0
    while i < len(data):
        cur = data[i]
        i += 1
        while i < len(data) and cur[0] == data[i]:
            cur += data[i]
            i += 1

        lst.append(cur)

    return lst


def say_what_you_see(mem, data):
    lst = split(data)
    cur = ""
    for item in lst:
        if item not in mem:
            mem[item] = str(len(item)) + item[0]
        cur += mem[item]

    return cur


def solve(puzzle_input, loop=40):
    current = puzzle_input
    mem = {}
    for _ in range(loop):
        current = say_what_you_see(mem, current)

    return len(current)


tst_input = "1"
puzzle_input = "3113322113"

print("Part 1")
p1_test = solve(tst_input, 5)
print(f"Test solution: {p1_test}.")
if p1_test == 6:
    print(f"Puzzle solution: {solve(puzzle_input)}.")

print()
print("Part 2")
p2_test = solve(tst_input, 50)
print(f"Test solution: {p2_test}.")
if p2_test == 1166642:
    print(f"Puzzle solution: {solve(puzzle_input, 50)}.")
