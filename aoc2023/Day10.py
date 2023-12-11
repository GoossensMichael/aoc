import Utils
from aocd import submit

day = 10
year = 2023
p1_expected_tst_result = 4
# test
p2_expected_tst_result = 1
# test2
# p2_expected_tst_result = 4
# test3
# p2_expected_tst_result = 7
# test4
# p2_expected_tst_result = 10
# test 5
# p2_expected_tst_result = 8
# test 6
# p2_expected_tst_result = 3

Utils.download_input(year, day)

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
mappings = {
    "|": {"U": (-1, 0), "D": (1, 0)},
    "-": {"R": (0, 1), "L": (0, -1)},
    "L": {"L": (-1, 0), "D": (0, 1)},
    "J": {"R": (-1, 0), "D": (0, -1)},
    "7": {"R": (1, 0), "U": (0, -1)},
    "F": {"U": (0, 1), "L": (1, 0)}
}
s_mappings = {
    "R": {"R": "-", "U": "J", "D": "7"},
    "L": {"L": "-", "U": "L", "D": "F"},
    "D": {"R": "L", "L": "J", "D": "|"},
    "U": {"R": "F", "L": "7", "U": "|"}
}
initial_d = {"|": "U", "-": "R", "L": "U", "J": "D", "7": "D", "F": "R"}
next_d = {
    ("U", "|"): "U",
    ("U", "F"): "R",
    ("U", "7"): "L",
    ("D", "|"): "D",
    ("D", "L"): "R",
    ("D", "J"): "L",
    ("L", "-"): "L",
    ("L", "F"): "D",
    ("L", "L"): "U",
    ("R", "-"): "R",
    ("R", "7"): "D",
    ("R", "J"): "U"
}

def start_positions(p):
    for d in directions:
        yield p[0] + d[0], p[1] + d[1]
    return None


def direction(p, c):
    if p[0] == c[0]:
        d = "R" if p[1] < c[1] else "L"
    else:
        d = "D" if p[0] < c[0] else "U"

    return d

def move(p, c):
    return c[0] - p[0], c[1] - p[1]


def get_next(p, c, maze):
    tile = maze[c[0]][c[1]]
    d_ = direction(p, c)

    if tile in mappings and d_ in mappings[tile]:
        d = mappings[tile][d_]
        return c[0] + d[0], c[1] + d[1]
    else:
        return None


def determine_s(s, m):
    s_n = [e for e in m if m[e] == 1 or m[e] == len(m) - 1]
    f = direction(s_n[0], s)
    t = direction(s, s_n[1])

    return s_mappings[f][t]

def get_tile(maze, c):
    return maze[c[0]][c[1]]


def in_bounds(maze, c):
    return 0 <= c[0] < len(maze) and 0 <= c[1] < len(maze[0])


def rotate_90(out):
    return -out[1], out[0]


def rotate_m90(out):
    return out[1], -out[0]

def calculate_group(s, m, maze):
    m_ = {m[p]: p for p in m if p != s}
    m_ = [m_[k] for k in sorted(m_.keys())]
    m_.append(s)

    group = set()

    prev = s
    for i in range(len(m_)):
        cur = m_[i]

        t = get_tile(maze, cur)
        mov = move(prev, cur)

        check = rotate_90(mov)
        out = (cur[0] + check[0], cur[1] + check[1])
        if in_bounds(maze, out) and get_tile(maze, out) == ".":
            group.add(out)

        # Needed to add this as in rare cases (1 in a hundred) a location would not be flagged when completely enclosed
        # by corner pieces. See test file 6 for a small example of it.
        if t in ("F", "7", "J", "L") and i + 1 < len(m_):
            nxt = m_[i+1]
            mov = move(cur, nxt)
            check = rotate_90(mov)
            out = (cur[0] + check[0], cur[1] + check[1])
            if in_bounds(maze, out) and get_tile(maze, out) == ".":
                group.add(out)

        prev = cur

    return group


def solve(data):
    maze = [[e for e in d] for d in data]
    s = find_start(maze)
    s_p = start_positions(s)

    loop = True
    while loop:
        m = dict()
        m[s] = 0

        p = s
        sp = next(s_p)
        r = sp
        while r is not None and r not in m:
            m[r] = m[p] + 1
            n = get_next(p, r, maze)
            if n is not None:
                p = r
            r = n

        if n == s or sp is None:
            loop = False

    empty_space = []
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if (i, j) not in m:
                #print(".", end="")
                empty_space.append((i, j))
                maze[i][j] = "."
            else:
                # Replace S with the correct one
                if maze[i][j] == "S":
                    s = (i, j)
                    maze[i][j] = determine_s((i, j), m)

    g = calculate_group(s, m, maze)
    todo = [i for i in g]
    while len(todo) > 0:
        n_todo = []
        for t in todo:
            for d in directions:
                n = t[0] + d[0], t[1] + d[1]
                if in_bounds(maze, n) and n not in g and get_tile(maze, n) == ".":
                    g.add(n)
                    n_todo.append(n)

        todo = n_todo

    o = (len(maze) * len(maze[0])) - len(m) - len(g)
    return ((max(m.values()) + 1) / 2, min(o, len(g)))


def find_start(maze):
    for i, r in enumerate(maze):
        for j, _ in enumerate(r):
            if maze[i][j] == "S":
                return i, j

    return None


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result[0]}.")
if p1_tst_result[0] == p1_expected_tst_result:
    print("Test passed - Calculating real input now")
    p1_result = solve(puzzle_input)
    submit(p1_result[0], part="a", day=day, year=year)
else:
    print("Test failed")

tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
print()
print("Part 2")
p2_tst_result = solve(tst_input)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result[1] == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    p2_result = p1_result
    submit(p2_result[1], part="b", day=day, year=year)
else:
    print("Test failed")
