from input import day1_input


def distance(position):
    return abs(position[0]) + abs(position[1])


def solve(directions):
    p = (0, 0)
    d = (0, 1)

    p2_found = False
    visited = {p: 1}

    for direction in directions:
        r, t = (direction[0], int(direction[1:]))
        if r == "R":
            d = (d[1], -d[0])
        elif r == "L":
            d = (-d[1], d[0])
        else:
            raise Exception("Impossible direction: " + direction + ".")

        if not p2_found:
            for _ in range(t):
                p = (p[0] + d[0], p[1] + d[1])
                visited[p] = visited.get(p, 0) + 1
                if (not p2_found and visited[p] == 2):
                    p2_found = True
                    print("Found first visited twice: " + str(p) + " with distance " + str(distance(p)) + ".")
        else:
            p = (p[0] + (t * d[0]), p[1] + (t * d[1]))

    print(distance(p))


solve(day1_input.puzzle_input.split(", "))
