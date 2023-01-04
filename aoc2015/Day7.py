import ctypes

import Utils
from input import day7_input


and_template = "% AND % -> %"
or_template = "% OR % -> %"
lshift_template = "% LSHIFT % -> %"
rshift_template = "% RSHIFT % -> %"
not_template = "NOT % -> %"
constant_template = "% -> %"


def b_id(wires, x, t):
    v = int(x) if x.isnumeric() else wires[x]()
    wires[t] = lambda: v
    return wires[t]()


def b_and(wires, x, y, t):
    v = (int(x) if x.isnumeric() else wires[x]()) & wires[y]()
    wires[t] = lambda: v
    return wires[t]()


def b_or(wires, x, y, t):
    v = (int(x) if x.isnumeric() else wires[x]()) | wires[y]()
    wires[t] = lambda: v
    return wires[t]()


def b_lshift(wires, x, y, t):
    v = wires[x]() << int(y)
    wires[t] = lambda: v
    return wires[t]()


def b_rshift(wires, x, y, t):
    v = wires[x]() >> int(y)
    wires[t] = lambda: v
    return wires[t]()


def b_not(wires, x, t):
    v = ctypes.c_uint16(~(wires[x]())).value
    wires[t] = lambda: v
    return wires[t]()


def parse_wires(wires, puzzle_input):
    for wiring in puzzle_input:
        if "AND" in wiring:
            l, r, t = Utils.extract_string(and_template, wiring)
            wires[t] = lambda x = l, y = r, k = t: b_and(wires, x, y, k)
        elif "OR" in wiring:
            l, r, t = Utils.extract_string(or_template, wiring)
            wires[t] = lambda x = l, y = r, k = t: b_or(wires, x, y, k)
        elif "LSHIFT" in wiring:
            l, r, t = Utils.extract_string(lshift_template, wiring)
            wires[t] = lambda x = l, y = r, k = t: b_lshift(wires, x, y, k)
        elif "RSHIFT" in wiring:
            l, r, t = Utils.extract_string(rshift_template, wiring)
            wires[t] = lambda x = l, y = r, k = t: b_rshift(wires, x, y, k)
        elif "NOT" in wiring:
            l, t = Utils.extract_string(not_template, wiring)
            wires[t] = lambda x = l, k = t: b_not(wires, x, k)
        elif "->" in wiring:
            l, t = Utils.extract_string(constant_template, wiring)
            wires[t] = lambda x = l, k = t: b_id(wires, x, k)


def solve(puzzle_input, wire, override=None):
    wires = {}
    parse_wires(wires, puzzle_input)

    solution = wires[wire]()
    print(wire + ": " + str(solution))

    if override is not None:
        wires = {}
        parse_wires(wires, puzzle_input)
        wires[override] = lambda x = str(solution), k = override: b_id(wires, x, k)
        print(wire + "(overridden): " + str(wires[wire]()))


tst_input = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""

solve(tst_input.splitlines(), "d")
solve(tst_input.splitlines(), "e")
solve(tst_input.splitlines(), "f")
solve(tst_input.splitlines(), "g")
solve(tst_input.splitlines(), "h")
solve(tst_input.splitlines(), "i")
solve(tst_input.splitlines(), "x")
solve(tst_input.splitlines(), "y")
print()
solve(day7_input.puzzle_input.splitlines(), "a", "b")
