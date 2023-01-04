import Utils
from input import day6_input

toggle_template = "toggle %,% through %,%"
turn_on_template = "turn on %,% through %,%"
turn_off_template = "turn off %,% through %,%"


def do_nothing(state): return state


def toggle(state): return (state + 1) % 2


def turn_on(_): return 1


def turn_off(_): return 0


state_changes_p1 = {
    "do_nothing": lambda state: state,
    "toggle": lambda state: (state + 1) % 2,
    "turn_on": lambda _: 1,
    "turn_off": lambda _: 0
}
state_changes_p2 = {
    "do_nothing": do_nothing,
    "toggle": lambda state: state + 2,
    "turn_on": lambda state: state + 1,
    "turn_off": lambda state: max(state - 1, 0)
}


def count(lights):
    n = 0
    for i in range(len(lights)):
        for j in range(len(lights[i])):
            n += lights[i][j]

    return n


def solve(puzzle_input, dimension, state_changes):
    lights = [[0] * dimension[0] for _ in range(dimension[1])]

    x_b, x_e, y_b, y_e = 0, 0, 0, 0
    for instruction in puzzle_input:
        operation = state_changes["do_nothing"]
        if instruction.startswith("toggle"):
            x_b, y_b, x_e, y_e = Utils.extract_int(toggle_template, instruction)
            operation = state_changes["toggle"]
        elif instruction.startswith("turn on"):
            x_b, y_b, x_e, y_e = Utils.extract_int(turn_on_template, instruction)
            operation = state_changes["turn_on"]
        elif instruction.startswith("turn off"):
            x_b, y_b, x_e, y_e = Utils.extract_int(turn_off_template, instruction)
            operation = state_changes["turn_off"]
        else:
            raise Exception("Instruction could not be parsed: {instruction}.")

        for x in range(x_b, x_e + 1):
            for y in range(y_b, y_e + 1):
                lights[x][y] = operation(lights[x][y])

    print(count(lights))


solve(day6_input.puzzle_input.splitlines(), (1000, 1000), state_changes_p1)
solve(day6_input.puzzle_input.splitlines(), (1000, 1000), state_changes_p2)
