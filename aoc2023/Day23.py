from aocd import submit

import Utils

day = 23
year = 2023
p1_expected_tst_result = 94
p2_expected_tst_result = 154

Utils.download_input(year, day)


directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
slopes = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}


def is_valid_move(n_position, d, path, maze, slippery):
    if n_position in path:
        return False
    tile = Utils.at_coord(maze, n_position)
    if tile == "#":
        return False
    if slippery and tile in slopes.keys():
        return slopes[tile] == d
    return True


def solve_p2(data, slippery=False):
    maze = Utils.tiles(data)

    start = (0, 1)
    end = (len(maze) - 1, len(maze[0]) - 2)
    node_searches = [(start, [(1, 0)])]
    nodes = {start: {}}

    while len(node_searches) > 0:
        node_search = node_searches.pop()

        for search_direction in node_search[1]:
            position = Utils.add_2d(node_search[0], search_direction)

            steps = 1
            valid_directions = [None]
            visited = {node_search[0], position}
            while len(valid_directions) == 1:
                valid_directions = []
                for d in directions:
                    n_position = Utils.add_2d(position, d)
                    if Utils.coord_valid(n_position, maze) and n_position not in visited and is_valid_move(n_position, d, [], maze, slippery):
                        valid_directions.append(d)

                if len(valid_directions) == 1:
                    position = Utils.add_2d(position, valid_directions[0])
                    visited.add(position)
                    steps += 1
                else:
                    if position not in nodes.keys():
                        node_searches.append((position, valid_directions))
                        nodes[position] = {}
                    if position in nodes[node_search[0]]:
                        nodes[node_search[0]][position] = max(nodes[node_search[0]][position], steps)
                    else:
                        nodes[node_search[0]][position] = steps
                    if position != end and not slippery:
                        nodes[position][node_search[0]] = steps

    finished_paths = []
    paths = [(0, [start], {start})]
    while len(paths) > 0:
        l, p, visited = paths.pop()

        next_nodes = [(k, v) for k, v in nodes[p[-1]].items() if k not in visited]
        if len(next_nodes) == 0 and p[-1] == end:
            finished_paths.append((l, p))
        else:
            for next_node, next_node_distance in next_nodes:
                paths.append((l - next_node_distance, p + [next_node], visited | {next_node}))

    return max([-l for l, p in finished_paths])


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve_p2(tst_input, True)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    print("Test passed - Calculating real input now")
    p1_result = solve_p2(puzzle_input, True)
    submit(p1_result, part="a", day=day, year=year)
else:
    print("Test failed")

print()
print("Part 2")
p2_tst_result = solve_p2(tst_input)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    p2_result = solve_p2(puzzle_input)
    submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")
