import time
import Utils
from aocd import submit

day = 17
year = 2024
p1_expected_tst_result = "4,6,3,5,6,3,5,2,1,0"
p2_expected_tst_result = 117440

Utils.download_input(year, day)


def parse(data):
    registers, program = data.split("\n\n")
    r_a, r_b, r_c = registers.split("\n")

    registers = {"A": Utils.extract_int("Register A: %", r_a)[0],
                 "B": Utils.extract_int("Register B: %", r_b)[0],
                 "C": Utils.extract_int("Register C: %", r_c)[0]}

    program = [int(x) for x in program.replace("Program: ", "").split(",")]

    return registers, program


def combo(operand, register):
    if 0 <= operand <= 3:
        combo_operand = operand
    elif operand == 4:
        combo_operand = register["A"]
    elif operand == 5:
        combo_operand = register["B"]
    elif operand == 6:
        combo_operand = register["C"]
    else:
        combo_operand = operand

    return combo_operand


def solve(register, program):
    i_p = 0
    out = []
    while i_p < len(program):
        opcode, operand = program[i_p:i_p+2]
        i_p += 2

        combo_operand = combo(operand, register)
        if opcode == 0:
            register["A"] = register["A"] >> combo_operand
        elif opcode == 1:
            register["B"] = register["B"] ^ operand
        elif opcode == 2:
            register["B"] = combo_operand % 8
        elif opcode == 3:
            if register["A"] > 0:
                i_p = operand
        elif opcode == 4:
            register["B"] = register["B"] ^ register["C"]
        elif opcode == 5:
            out.append(combo_operand % 8)
        elif opcode == 6:
            register["B"] = register["A"] >> combo_operand
        elif opcode == 7:
            register["C"] = register["A"] >> combo_operand

    return out


def solve1(data):
    register, program = parse(data)
    return ",".join(map(str, solve(register, program)))


def matching_score(program, solution):
    i = 0
    while i < len(program) and i < len(solution) and program[i] == solution[i]:
        i += 1

    return i


def solve2(data):
    register, program = parse(data)

    work = [(len(program) - 1, 0)]
    while work:
        i, previous_r_a = work.pop(0)
        for bits in range(8):
            r_a = previous_r_a + bits
            r = {"A": r_a, "B": register["B"], "C": register["C"]}
            output = solve(r, program)
            if output == program[i:]:
                if i == 0:
                    work.clear()
                    break
                elif i > 0:
                    work.append((i-1, r_a * 8))

    return r_a


if __name__ == "__main__":
    tst_input = Utils.read_input_flat(f"input/day{day}_tst_input.txt")
    tst2_input = Utils.read_input_flat(f"input/day{day}_tst2_input.txt")
    puzzle_input = Utils.read_input_flat(f"input/day{day}_input.txt")

    print("Part 1")
    start_time = time.time()
    p1_tst_result = solve1(tst_input)
    print(f"Test solution: {p1_tst_result}.")
    elapsed_time = time.time() - start_time
    print(f"Time taken p1 test: {elapsed_time:.2f} seconds")
    if p1_tst_result == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p1_result = solve1(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p1: {elapsed_time:.2f} seconds")
        submit(p1_result, part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    start_time = time.time()
    p2_tst_result = solve2(tst2_input)
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
