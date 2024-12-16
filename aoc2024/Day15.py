import time
import Utils
from aocd import submit

day = 15
year = 2024
p1_expected_tst_result = 10092
p2_expected_tst_result = 9021

Utils.download_input(year, day)


directions = {"<": (0, -1), "v": (1, 0), ">": (0, 1), "^": (-1, 0)}


def find_robot(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == "@":
                return i, j


def multiply(j):
    if j == "@":
        return "@."
    elif j == ".":
        return ".."
    elif j == "#":
        return "##"
    else:
        return "[]"


def parse(data, double=False):
    m_d, i_d = data.split("\n\n")
    m = m_d.split("\n")

    r_m = []
    for i in range(len(m)):
        if double:
            line = []
            for j in m[i]:
                a, b = multiply(j)
                line.append(a)
                line.append(b)
            r_m.append(line)
        else:
            r_m.append([j for j in m[i]])

    return r_m, find_robot(r_m), i_d.replace("\n", "")


def calc_coordinate(m):
    return sum([(i * 100 + j) for j in range(len(m[0])) for i in range(len(m)) if m[i][j] in ("O", "[")])


def find_free_spot(m, p, d):
    search = True

    result = None
    while search:
        x, y = p[0] + d[0], p[1] + d[1]

        if m[x][y] == ".":
            result = x, y
            search = False
        elif m[x][y] == "#":
            search = False
        else:
            p = x, y

    return result


def perform_move(m, p, move):
    x_d, y_d = directions[move]

    x, y = p
    x_n, y_n = x + x_d, y + y_d
    if m[x_n][y_n] == ".":
        m[x_n][y_n] = "@"
        m[x][y] = "."
    elif m[x_n][y_n] == "#":
        x_n = x
        y_n = y
    else:
        p_b = find_free_spot(m, (x_n, y_n), (x_d, y_d))
        if p_b is not None:
            m[p_b[0]][p_b[1]] = "O"
            m[x_n][y_n] = "@"
            m[x][y] = "."
        else:
            x_n = x
            y_n = y

    return x_n, y_n


def solve(data):
    map_data, position, moves = parse(data)

    for i in range(len(moves)):
        move = moves[i]
        position = perform_move(map_data, position, move)

    return calc_coordinate(map_data)


def other_half(m, p_x, p_y):
    if m[p_x][p_y] == "[" and m[p_x][p_y + 1] == "]":
        o_y = p_y + 1
    elif m[p_x][p_y] == "]" and m[p_x][p_y - 1] == "[":
        o_y = p_y - 1
    else:
        o_y = p_y

    return o_y


def try_to_move(m, d_x, box_parts, mappings, moved):
    move = True
    while move and box_parts:
        b_x, b_y = box_parts.pop()
        n_b_x = b_x + d_x

        if m[n_b_x][b_y] == "#":
            move = False
        elif m[n_b_x][b_y] == ".":
            mappings.append((n_b_x, b_y, m[b_x][b_y]))
            mappings.append((b_x, b_y, "."))
        else:
            o_y = other_half(m, n_b_x, b_y)

            to_move = []
            if (n_b_x, b_y) not in moved:
                to_move.append((n_b_x, b_y))
                moved.add((n_b_x, b_y))
            if (n_b_x, o_y) not in moved:
                to_move.append((n_b_x, o_y))
                moved.add((n_b_x, o_y))
            move = try_to_move(m, d_x, to_move, mappings, moved)
            if move:
                mappings.append((n_b_x, b_y, m[b_x][b_y]))
                mappings.append((b_x, b_y, "."))

    return move


def find_v_free_spot(m, p, d_x):
    p_x, p_y = p
    if m[p_x][p_y] == ".":
        return True
    elif m[p_x][p_y] == "#":
        return False

    o_y = other_half(m, p_x, p_y)
    mappings = []
    moved = set()
    moved.add((p_x, p_y))
    moved.add((p_x, o_y))
    apply = try_to_move(m, d_x, [(p_x, p_y), (p_x, o_y)], mappings, moved)

    if apply:
        for x, y, v in mappings:
            m[x][y] = v

    return apply


def find_h_free_spot(m, p, d_y):
    search = True

    p_x, p_y = p
    y = p_y
    while search:
        if m[p_x][y] == "#":
            return False
        elif m[p_x][y] == ".":
            search = False
        else:
            y = y + d_y

    for y_l in range(y, p_y, -d_y):
        m[p_x][y_l] = m[p_x][y_l - d_y]
        m[p_x][y_l - d_y] = "."

    return True


def perform_move2(m, p, move):
    x_d, y_d = directions[move]

    x, y = p
    x_n, y_n = x + x_d, y + y_d
    if m[x_n][y_n] == ".":
        m[x_n][y_n] = "@"
        m[x][y] = "."
    elif m[x_n][y_n] == "#":
        x_n = x
        y_n = y
    else:
        if move in ("v", "^"):
            found_free_spot = find_v_free_spot(m, (x_n, y_n), x_d)
        else:
            found_free_spot = find_h_free_spot(m, (x_n, y_n), y_d)

        if found_free_spot:
            m[x_n][y_n] = "@"
            m[x][y] = "."
        else:
            x_n, y_n = x, y

    return x_n, y_n


def solve2(data):
    map_data, position, moves = parse(data, True)

    for i in range(len(moves)):
        move = moves[i]
        position = perform_move2(map_data, position, move)

    return calc_coordinate(map_data)


if __name__ == "__main__":
    tst_input = Utils.read_input_flat(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input_flat(f"input/day{day}_input.txt")

    print("Part 1")
    start_time = time.time()
    p1_tst_result = solve(tst_input)
    print(f"Test solution: {p1_tst_result}.")
    elapsed_time = time.time() - start_time
    print(f"Time taken p1 test: {elapsed_time:.2f} seconds")
    if p1_tst_result == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p1_result = solve(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p1: {elapsed_time:.2f} seconds")
        submit(p1_result, part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    start_time = time.time()
    p2_tst_result = solve2(tst_input)
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p2_result = solve2(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
