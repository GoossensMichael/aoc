from difflib import SequenceMatcher
import ctypes

from input import day7_input


and_template = "% AND % -> %"
or_template = "% OR % -> %"
lshift_template = "% LSHIFT % -> %"
rshift_template = "% RSHIFT % -> %"
not_template = "NOT % -> %"
constant_template = "% -> %"


def extract(template, text):
    seq = SequenceMatcher(None, template, text, True)
    return [text[c:d] for tag, a, b, c, d in seq.get_opcodes() if tag == 'replace']


def b(wires, x, t):
    v = int(x) if x.isnumeric() else wires[x]()
    wires[t] = lambda: v
    return wires[t]()


def bAnd(wires, x, y, t):
    v = (int(x) if x.isnumeric() else wires[x]()) & wires[y]()
    wires[t] = lambda: v
    return wires[t]()


def bOr(wires, x, y, t):
    v = (int(x) if x.isnumeric() else wires[x]()) | wires[y]()
    wires[t] = lambda: v
    return wires[t]()


def bLShift(wires, x, y, t):
    v = wires[x]() << int(y)
    wires[t] = lambda: v
    return wires[t]()


def bRShift(wires, x, y, t):
    v = wires[x]() >> int(y)
    wires[t] = lambda: v
    return wires[t]()


def bNot(wires, x, t):
    v = ctypes.c_uint16(~(wires[x]())).value
    wires[t] = lambda: v
    return wires[t]()


def parseWires(wires, puzzle_input):
    for wiring in puzzle_input:
        if "AND" in wiring:
            l, r, t = extract(and_template, wiring)
            wires[t] = lambda x = l, y = r, k = t: bAnd(wires, x, y, k)
            #wires[t] = lambda x = l, y = r: (int(x) if x.isnumeric() else wires[x]()) & wires[y]()
        elif "OR" in wiring:
            l, r, t = extract(or_template, wiring)
            wires[t] = lambda x = l, y = r, k = t: bOr(wires, x, y, k)
            #wires[t] = lambda x = l, y = r: wires[x]() | wires[y]()
        elif "LSHIFT" in wiring:
            l, r, t = extract(lshift_template, wiring)
            wires[t] = lambda x = l, y = r, k = t: bLShift(wires, x, y, k)
            #wires[t] = lambda x = l, y = r: wires[x]() << int(y)
        elif "RSHIFT" in wiring:
            l, r, t = extract(rshift_template, wiring)
            wires[t] = lambda x = l, y = r, k = t: bRShift(wires, x, y, k)
            #wires[t] = lambda x = l, y = r: wires[x]() >> int(y)
        elif "NOT" in wiring:
            l, t = extract(not_template, wiring)
            wires[t] = lambda x = l, k = t: bNot(wires, x, k)
            #wires[t] = lambda x = l: ~(wires[x]())
        elif "->" in wiring:
            l, t = extract(constant_template, wiring)
            wires[t] = lambda x = l, k = t: b(wires, x, k)
            #wires[t] = lambda x = l: int(x) if x.isnumeric() else wires[x]()
        else:
            raise Exception("Did not expect wiring to be: " + wiring + ".")


def solve(puzzle_input, wire, override=None):
    wires = {}

    parseWires(wires, puzzle_input)

    wire_value = wires[wire]()
    print(wire + ": " + str(wire_value))

    if override is not None:
        new_wires = {}
        parseWires(new_wires, puzzle_input)
        new_wires[override] = lambda x = str(wire_value), k = override: b(new_wires, x, k)
        print(wire + "(overridden): " + str(new_wires[wire]()))



tst_input = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""

tst_input2 = """123 -> x
NOT x -> y
"""

t1 = ctypes.c_uint16(~123).value
print("Binary: " + str(t1))

solve(tst_input2.splitlines(), "y")
print()
solve(tst_input.splitlines(), "d")
solve(tst_input.splitlines(), "e")
solve(tst_input.splitlines(), "f")
solve(tst_input.splitlines(), "g")
solve(tst_input.splitlines(), "h")
solve(tst_input.splitlines(), "i")
solve(tst_input.splitlines(), "x")
solve(tst_input.splitlines(), "y")
print()
solve(day7_input.puzzle_input.splitlines(), "a")
solve(day7_input.puzzle_input.splitlines(), "a", "b")

# Expected values for tst_input:
# d: 72
# e: 507
# f: 492
# g: 114
# h: 65412
# i: 65079
# x: 123
# y: 456
