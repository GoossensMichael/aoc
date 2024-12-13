import time
import Utils
from aocd import submit

day = 13
year = 2024
p1_expected_tst_result = 480
p2_expected_tst_result = 875318608908

Utils.download_input(year, day)


def parse(data, adjustment):
    machines = []
    for machine_config in data.split("\n\n"):
        config_a, config_b, config_prize = machine_config.split("\n")

        machine = {"A": Utils.extract_int("Button A: X+%, Y+%", config_a),
                   "B": Utils.extract_int("Button B: X+%, Y+%", config_b),
                   "P": Utils.extract_int("Prize: X=%, Y=%", config_prize)}
        if adjustment != 0:
            machine["P"] = machine["P"][0] + adjustment, machine["P"][1] + adjustment

        machines.append(machine)

    return machines

def find_steps(machine):
    ax, ay = machine["A"]
    bx, by = machine["B"]
    tx, ty = machine["P"]

    det = ax * by - ay * bx

    if det == 0:
        return None

    # Solve the linear system using Cramer's rule
    dx = tx * by - ty * bx
    dy = ax * ty - ay * tx

    if dx % det != 0 or dy % det != 0:
        # No integer solution exists
        return None

    n_a = dx // det
    n_b = dy // det

    return n_a, n_b


def solve(data, adjustment=0):
    machines = parse(data, adjustment)

    tokens = 0
    for machine in machines:
        solution = find_steps(machine)
        if solution is not None:
            a_pushes, b_pushes = solution
            tokens += (a_pushes * 3) + b_pushes

    return tokens


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

    adjustment = 10000000000000
    print()
    print("Part 2")
    start_time = time.time()
    p2_tst_result = solve(tst_input, adjustment)
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p2_result = solve(puzzle_input, adjustment)
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
