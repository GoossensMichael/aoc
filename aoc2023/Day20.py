from abc import abstractmethod
from enum import Enum, auto

import Utils
from aocd import submit

day = 20
year = 2023
p1_expected_tst_result = 32000000
p2_expected_tst_result = 1

Utils.download_input(year, day)


class State(Enum):
    ON = auto()
    OFF = auto()

class Pulse(Enum):
    HIGH = auto()
    LOW = auto()


class Module:

    def __init__(self, name, targets):
        self.name = name
        self.targets = targets

    @abstractmethod
    def receive(self, pulse, origin):
        pass

class Sink(Module):

    def receive(selfs, _, __):
        return []

class Broadcaster(Module):

    def receive(self, pulse, _):
        return [(target, pulse, self.name) for target in self.targets]

class FlipFlop(Module):

    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.state = State.OFF

    def receive(self, pulse, _):
        if pulse == Pulse.LOW:
            if self.state == State.OFF:
                self.state = State.ON
                return [(target, Pulse.HIGH, self.name) for target in self.targets]
            else:
                self.state = State.OFF
                return [(target, Pulse.LOW, self.name) for target in self.targets]
        else:
            return []


class Conjunction(Module):

    def __init__(self, name, targets):
        super().__init__(name, targets)
        self.mem = {}

    def add_input(self, input):
        self.mem[input] = Pulse.LOW

    def get_exit_pulse(self):
        if len([1 for mem_value in self.mem.values() if mem_value == Pulse.LOW]) > 0:
            return Pulse.HIGH
        else:
            return Pulse.LOW

    def receive(self, pulse, origin):
        self.mem[origin] = pulse
        exit_pulse = self.get_exit_pulse()
        return [(target, exit_pulse, self.name) for target in self.targets]

def parse(data):
    inputs_by_module = {}
    modules = {}
    for d in data:
        m, mapping = d.split(" -> ")
        mapping = mapping.split(", ")
        if m[0] == "%":
            m = m[1:]
            modules[m] = FlipFlop(m, mapping)
        elif m[0] == "&":
            m = m[1:]
            modules[m] = Conjunction(m, mapping)
        else:
            modules[m] = Broadcaster(m, mapping)

        for module in mapping:
            if module not in inputs_by_module:
                inputs_by_module[module] = []
            inputs_by_module[module].append(m)

    for module_input in inputs_by_module.keys():
        if module_input not in modules:
            modules[module_input] = Sink(module_input, None)
        elif type(modules[module_input]) is Conjunction:
            for input in inputs_by_module[module_input]:
                modules[module_input].add_input(input)

    if "rx" in inputs_by_module:
        conjunction = modules[inputs_by_module["rx"][0]]
    else:
        conjunction = None

    return modules, conjunction


def solve(data, button_presses = 1000):
    modules, conjunction = parse(data)
    conjunction_results = {}

    cnt_l = 0
    cnt_h = 0
    for button_press in range(button_presses):
        pulses = modules["broadcaster"].receive(Pulse.LOW, None)
        cnt_l += sum([1 for _, p, _ in pulses if p == Pulse.LOW]) + 1
        cnt_h += sum([1 for _, p, _ in pulses if p == Pulse.HIGH])

        while len(pulses) > 0:
            n_pulses = []
            for pulse in pulses:
                n_pulses.extend(modules[pulse[0]].receive(pulse[1], pulse[2]))
            pulses = n_pulses
            cnt_l += sum([1 for _, p, _ in pulses if p == Pulse.LOW])
            cnt_h += sum([1 for _, p, _ in pulses if p == Pulse.HIGH])

            if conjunction is not None:
                for f in conjunction.mem:
                    if (conjunction.name, Pulse.HIGH, f) in pulses and f not in conjunction_results:
                        conjunction_results[f] = button_press + 1

    return cnt_l * cnt_h, mul(conjunction_results.values())


def mul(values):
    m = 1
    for v in values:
        m *= v
    return m


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")


print("Part 1")
p1_tst_result = solve(tst_input)[0]
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    print("Test passed - Calculating real input now")
    p1_result = solve(puzzle_input)[0]
    submit(p1_result, part="a", day=day, year=year)
else:
    print("Test failed")

print()
print("Part 2")
p2_tst_result = solve(tst_input, 1)[1]
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    p2_result = solve(puzzle_input, 5000)[1]
    if p2_result > 0:
      submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")
