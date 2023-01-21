import Utils

day = 17


# Paths is a list of tuples containing the current count and index of the last container added.
# Solutions are those tuples with the current count matching target_value (Could later include a list of the path)
# Containers is the input data with all possible containers
# Target value is the amount to match
#
# Is this fast enough?
def travel(paths, solutions, containers, target_value):
    while len(paths) > 0:
        if len(paths) == 0 and len(solutions) > 0:
            return solutions
        else:
            current_path = paths.pop()
            for i in range(current_path[2], len(containers)):
                new_path = list(current_path[0])
                new_path.append(containers[i])
                weight = current_path[1] + containers[i]
                if weight < target_value:
                    paths.append((new_path, weight, i+1))
                elif weight == target_value:
                    solutions.append(new_path)

    return solutions


def solve(data, liters):
    containers = [int(size) for size in data]

    solutions = travel([([], 0, 0)], [], containers, liters)

    minimum_container_amount = len(solutions[0])
    amount_of_min = 0
    for solution in solutions:
        if len(solution) < minimum_container_amount:
            minimum_container_amount = len(solution)
            amount_of_min = 1
        elif len(solution) == minimum_container_amount:
            amount_of_min += 1

    return len(solutions), amount_of_min


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_test = solve(tst_input, 25)
print(f"Test solution: {p1_test[0]}.")
if p1_test[0] == 4:
    p1 = solve(puzzle_input, 150)
    print(f"Puzzle solution: {p1[0]}.")

print()
print("Part 2")
p2_test = p1_test[1]
print(f"Test solution: {p2_test}.")
if p2_test == 3:
    print(f"Puzzle solution: {solve(puzzle_input, 150)[1]}.")
