from input import day12_input


def solve(data, exclude_red=False):
    acc = 0
    if type(data) == list:
        acc += sum([solve(field, exclude_red) for field in data])
    elif type(data) == dict:
        if exclude_red is False or "red" not in data.values():
            acc += sum([solve(value, exclude_red) for value in data.values()])
    elif type(data) == int:
        acc += data

    return acc


tst_input = ([1,2,3], {"a":2,"b":4}, [[[3]]], {"a":{"b":4},"c":-1}, {"a":[-1,1]}, [-1,{"a":1}], [], {})
puzzle_input = day12_input.puzzle_input

print("Part 1")
p1_test = [solve(test) for test in tst_input]
print(f"Test solution: {p1_test}.")
if p1_test == [6, 6, 3, 3, 0, 0, 0, 0]:
    p1 = solve(puzzle_input)
    print(f"Puzzle solution: {p1}.")

tst_input = ([1, 2, 3], [1, {"c": "red", "b": 2}, 3], {"d": "red", "e": [1, 2, 3, 4], "f": 5}, [1, "red", 5])
print()
print("Part 2")
p2_test = [solve(test, True) for test in tst_input]
print(f"Test solution: {p2_test}.")
if p2_test == [6, 4, 0, 6]:
    print(f"Puzzle solution: {solve(puzzle_input, True)}.")
