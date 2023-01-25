import Utils

day = 18


def get_neighbours(light_board, position):
    neighbours = {"on": [], "off": []}

    dim = len(light_board)
    for i in range(max(0, position[0] - 1), min(dim, position[0] + 2)):
        for j in range(max(0, position[1] - 1), min(dim, position[1] + 2)):
            if i != position[0] or j != position[1]:
                if light_board[i][j] == 0:
                    neighbours["off"].append((i, j))
                else:
                    neighbours["on"].append((i, j))

    return neighbours


def step(light_board, fixed_corners):
    dim = len(light_board)
    new_light_board = [[0] * dim for _ in range(dim)]

    for i in range(dim):
        for j in range(dim):
            neighbours = get_neighbours(light_board, (i, j))
            if light_board[i][j] == 0:
                if len(neighbours["on"]) == 3:
                    new_light_board[i][j] = 1
                else:
                    new_light_board[i][j] = 0
            else:
                if len(neighbours["on"]) >= 2 and len(neighbours["on"]) <= 3:
                    new_light_board[i][j] = 1
                else:
                    new_light_board[i][j] = 0

    if fixed_corners:
        new_light_board[0][0] = 1
        new_light_board[dim - 1][0] = 1
        new_light_board[0][dim - 1] = 1
        new_light_board[dim - 1][dim - 1] = 1

    return new_light_board


def count(light_board, state):
    count = 0
    for line in light_board:
        for light in line:
            if light == state:
                count += 1

    return count


def solve(data, steps=100, fixed_corners=False):
    dim = len(data[0])

    light_board = [[0] * dim for _ in range(dim)]

    if fixed_corners:
        light_board[0][0] = 1
        light_board[dim - 1][0] = 1
        light_board[0][dim - 1] = 1
        light_board[dim - 1][dim - 1] = 1

    for i in range(len(data)):
        for j in range(len(data[i])):
            match data[i][j]:
                case "#":
                    light_board[i][j] = 1

    for i in range(steps):
        light_board = step(light_board, fixed_corners)

    return count(light_board, 1)


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_test = solve(tst_input, 4)
print(f"Test solution: {p1_test}.")
if p1_test == 4:
    p1 = solve(puzzle_input)
    print(f"Puzzle solution: {p1}.")

print()
print("Part 2")
p2_test = solve(tst_input, 5, True)
print(f"Test solution: {p2_test}.")
if p2_test == 17:
    print(f"Puzzle solution: {solve(puzzle_input, fixed_corners=True)}.")
