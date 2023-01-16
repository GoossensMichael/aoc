import Utils

day = 2

key_pad_p1 = [["0", "0", "0", "0", "0"],
              ["0", "1", "2", "3", "0"],
              ["0", "4", "5", "6", "0"],
              ["0", "7", "8", "9", "0"],
              ["0", "0", "0", "0", "0"]]

key_pad_p2 = [["0", "0", "0", "0", "0", "0", "0"],
              ["0", "0", "0", "1", "0", "0", "0"],
              ["0", "0", "2", "3", "4", "0", "0"],
              ["0", "5", "6", "7", "8", "9", "0"],
              ["0", "0", "A", "B", "C", "0", "0"],
              ["0", "0", "0", "D", "0", "0", "0"],
              ["0", "0", "0", "0", "0", "0", "0"]]


def solve(data, start_position, key_pad):
    position = (start_position[0], start_position[1])

    solution = []
    for instructions in data:
        for instruction in instructions:
            d = (0, 0)
            match instruction:
                case "U":
                    d = (-1, 0)
                case "R":
                    d = (0, 1)
                case "D":
                    d = (1, 0)
                case "L":
                    d = (0, -1)

            new_position = (position[0] + d[0], position[1] + d[1])
            if key_pad[new_position[0]][new_position[1]] != "0":
                position = new_position

        solution.append(key_pad[position[0]][position[1]])

    return "".join(solution)


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_test = solve(tst_input, (2, 2), key_pad_p1)
print(f"Test solution: {p1_test}.")
if p1_test == "1985":
    p1 = solve(puzzle_input, (2, 2), key_pad_p1)
    print(f"Puzzle solution: {p1}.")

print()
print("Part 2")
p2_test = solve(tst_input, (3, 1), key_pad_p2)
print(f"Test solution: {p2_test}.")
if p2_test == "5DB3":
    print(f"Puzzle solution: {solve(puzzle_input, (3, 1), key_pad_p2)}.")
