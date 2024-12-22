import time
import Utils
from aocd import submit

day = 21
year = 2024
p1_expected_tst_result = 126384
p2_expected_tst_result = -1

Utils.download_input(year, day)


u = (-1, 0)
r = (0, 1)
d = (1, 0)
l = (0, -1)
a = "A"


"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""
n_to_d = {
    (1, 1): [], (1, 2): [r], (1, 3): [r, r], (1, 4): [u], (1, 5): [r, u], (1, 6): [r, r, u],
    (1, 7): [u, u], (1, 8): [r, u, u], (1, 9): [r, r, u, u], (1, 0): [r, d], (1, a): [r, r, d],
    (2, 1): [l], (2, 2): [], (2, 3): [r], (2, 4): [l, u], (2, 5): [u], (2, 6): [r, u],
    (2, 7): [l, u, u], (2, 8): [u, u], (2, 9): [r, u, u], (2, 0): [d], (2, a): [r, d],
    (3, 1): [l, l], (3, 2): [l], (3, 3): [], (3, 4): [l, l, u], (3, 5): [l, u], (3, 6): [u],
    (3, 7): [l, l, u, u], (3, 8): [l, u, u], (3, 9): [u, u], (3, 0): [l, d], (3, a): [d],
    (4, 1): [d], (4, 2): [r, d], (4, 3): [r, r, d], (4, 4): [], (4, 5): [r], (4, 6): [r, r],
    (4, 7): [u], (4, 8): [r, u], (4, 9): [r, r, u], (4, 0): [r, d, d], (4, a): [r, r, d, d],
    (5, 1): [l, d], (5, 2): [d], (5, 3): [r, d], (5, 4): [l], (5, 5): [], (5, 6): [r],
    (5, 7): [l, u], (5, 8): [u], (5, 9): [r, u], (5, 0): [d, d], (5, a): [r, d, d],
    (6, 1): [l, l, d], (6, 2): [l, d], (6, 3): [d], (6, 4): [l, l], (6, 5): [l], (6, 6): [],
    (6, 7): [u, l, l], (6, 8): [u, l], (6, 9): [u], (6, 0): [l, d, d], (6, a): [d, d],
    (7, 1): [d, d], (7, 2): [r, d, d], (7, 3): [r, r, d, d], (7, 4): [d], (7, 5): [r, d], (7, 6): [r, r, d],
    (7, 7): [], (7, 8): [r], (7, 9): [r, r], (7, 0): [l, d, d, d], (7, a): [l, l, d, d, d],
    (8, 1): [l, d, d], (8, 2): [d, d], (8, 3): [r, d, d], (8, 4): [l, d], (8, 5): [d], (8, 6): [r, d],
    (8, 7): [l], (8, 8): [], (8, 9): [r], (8, 0): [d, d, d], (8, a): [r, d, d, d],
    (9, 1): [l, l, d, d], (9, 2): [l, d, d], (9, 3): [d, d], (9, 4): [l, l, d], (9, 5): [l, d], (9, 6): [d],
    (9, 7): [l, l], (9, 8): [l], (9, 9): [], (9, 0): [d, l, d, d], (9, a): [d, d, d],
    (0, 1): [u, l], (0, 2): [u], (0, 3): [u, r], (0, 4): [u, u, l], (0, 5): [u, u], (0, 6): [u, u, r],
    (0, 7): [u, u, u, l], (0, 8): [u, u, u], (0, 9): [u, u, u, r], (0, 0): [], (0, a): [r],
    (a, 1): [u, l, l], (a, 2): [u, l], (a, 3): [u], (a, 4): [u, u, l, l], (a, 5): [u, u, l], (a, 6): [u, u],
    (a, 7): [u, u, u, l, l], (a, 8): [u, u, u, l], (a, 9): [u, u, u], (a, 0): [l], (a, a): []
}

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""
d_to_d = {
    (u, u): [], (u, r): [d, r], (u, d): [d], (u, l): [d, l], (u, a): [r],
    (r, u): [u, l], (r, r): [], (r, d): [l], (r, l): [l, l], (r, a): [u],
    (d, u): [u], (d, r): [r], (d, d): [], (d, l): [l], (d, a): [r, u],
    (l, u): [r, u], (l, r): [r, r], (l, d): [r], (l, l): [], (l, a): [r, r, u],
    (a, u): [l], (a, r): [d], (a, d): [l, d], (a, l): [d, l, l], (a, a): []
}


def to_symbol(c):
    if c == (1, 0):
        return "v"
    elif c == (0, 1):
        return ">"
    elif c == (-1, 0):
        return "^"
    elif c == (0, -1):
        return "<"
    else:
        return "A"

def print_symbols(n, sequence, prefix=""):
    # return
    for m in sequence:
        print(prefix + str(n) + ": " + "".join([to_symbol(n) for n in m]))


def to_symbol_sequence(sequence):
    moves = []
    for m in sequence:
        for n in m:
            moves.append(to_symbol(n))

    return moves


def remove_empty(l):
    return [e for e in l if e != []]


def solve(data):
    solutions = []

    r1 = a
    r2 = a
    r3 = a
    for password in data:
        print(f"Calculating for key code {password}")
        sequence = []
        for code in password:
            n = a if code == a else int(code)

            r1_sequence = [n_to_d[(r1, n)], [a]]
            r1 = n
            print_symbols(n, r1_sequence)

            r2_sequence = []
            for s in r1_sequence:
                for m in s:
                    r2_sequence.extend(remove_empty([d_to_d[(r2, m)], [a]]))
                    r2 = m
            print_symbols(n, r2_sequence, "\t")

            r3_sequence = []
            for s in r2_sequence:
                for m in s:
                    r3_sequence.extend(remove_empty([d_to_d[(r3, m)], [a]]))
                    r3 = m
            print_symbols(n, r3_sequence, "\t\t")

            sequence.extend(r3_sequence)
        print()

        solutions.append((password, to_symbol_sequence(sequence)))

        print("".join(solutions[0][1]))

    return sum([int(code[:-1]) * len(sequence) for code, sequence in solutions])

"""
029A <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
     v<<A>>^A<A>AvA<^AA>A<vAAA>^A
     <A^A>^^AvvvA
     029A
     
mine v<<A>>^AvA^Av<<A>>^AA<vA<A>>^AAvAA<^A>A<vA^>AA<A>Av<<A>A^>AAA<Av>A^A
     <v<A>>^AvA^A <vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
     
     
     <vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
"""

if __name__ == "__main__":
    tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

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

    # print()
    # print("Part 2")
    # start_time = time.time()
    # p2_tst_result = solve(tst_input)
    # elapsed_time = time.time() - start_time
    # print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    # print(f"Test solution: {p2_tst_result}.")
    # if p2_tst_result == p2_expected_tst_result:
    #     print("Test passed - Calculating real input now")
    #     start_time = time.time()
    #     p2_result = solve(puzzle_input)
    #     elapsed_time = time.time() - start_time
    #     print(f"Time taken p2: {elapsed_time:.2f} seconds")
    #     submit(p2_result, part="b", day=day, year=year)
    # else:
    #     print("Test failed")
