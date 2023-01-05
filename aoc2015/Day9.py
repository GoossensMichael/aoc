import bisect

import Utils

template = "% to % = %"


def parse_input(lines):
    routes = {}
    destinations = set()
    for line in lines:
        f, t, d = Utils.extract_string(template, line)
        routes[(f, t)] = int(d)
        routes[(t, f)] = int(d)
        destinations.add(f)
        destinations.add(t)

    return dict(sorted(routes.items(), key=lambda p: p[1])), destinations


def get_next_visits(path, routes):
    next_visits = []
    for route in routes:
        if path[0][-1] == route[0] and route[1] not in path[0]:

            next_visit = (route[1], routes[route])
            next_visits.append(next_visit)

    return next_visits


def travel_p1(paths, routes, amount_of_destinations):
    shortest_path = ([], 0)

    while amount_of_destinations > len(shortest_path[0]):
        shortest_path = paths.pop(0)

        next_visits = get_next_visits(shortest_path, routes)
        for next_visit in next_visits:
            new_path = (shortest_path[0] + [next_visit[0]], shortest_path[1] + next_visit[1])
            bisect.insort(paths, new_path, key=lambda p: p[1])

    return shortest_path


def travel_p2(paths, routes, amount_of_destinations):
    result = []

    while any(len(path[0]) < amount_of_destinations for path in paths):
        longest_path = paths.pop(-1)

        if len(longest_path[0]) == amount_of_destinations:
            bisect.insort(result, longest_path, key=lambda p: p[1])
        else:
            next_visits = get_next_visits(longest_path, routes)
            for next_visit in next_visits:
                new_path = (longest_path[0] + [next_visit[0]], longest_path[1] + next_visit[1])
                bisect.insort(paths, new_path, key=lambda p: p[1])

    return result[-1]


def solve(lines, travel_method):
    routes, destinations = parse_input(lines)

    initial_paths = [([f, t], routes[f, t]) for f, t in routes]
    shortest_path = travel_method(initial_paths, dict(routes), len(destinations))

    return shortest_path[1]


tst_input = Utils.read_input("input/day9_tst_input.txt")
puzzle_input = Utils.read_input("input/day9_input.txt")

print("Part 1")
p1_test = solve(tst_input, travel_p1)
print(f"Test solution: {p1_test}.")
if p1_test == 605:
    print(f"Puzzle solution: {solve(puzzle_input, travel_p1)}.")

print()
print("Part 2")
p2_test = solve(tst_input, travel_p2)
print(f"Test solution: {p2_test}.")
if p2_test == 982:
    print(f"Puzzle solution: {solve(puzzle_input, travel_p2)}.")
