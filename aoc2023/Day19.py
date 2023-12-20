from abc import abstractmethod
import copy
import Utils
from aocd import submit

day = 19
year = 2023
p1_expected_tst_result = 19114
p2_expected_tst_result = 167409079868000

Utils.download_input(year, day)


class Operation:

    def __init__(self, result_on_match):
        self.result_on_match = result_on_match

    @abstractmethod
    def apply(self, part):
        pass

    @abstractmethod
    def search_ranges(self, workflows, part):
        pass


class Constant(Operation):

    def apply(self, part):
        return self.result_on_match

    def search_ranges(self, workflows, part):
        if self.result_on_match == "A":
            return [part]
        elif self.result_on_match != "R":
            return workflows[self.result_on_match].search_ranges(workflows, part)
        else:
            return []


class CompareOperation(Operation):

    def __init__(self, property, value, result_on_match, next_operation):
        super().__init__(result_on_match)
        self.property = property
        self.value = value
        self.next_operation = next_operation


class LessThan(CompareOperation):

    def apply(self, part):
        return self.result_on_match if part[self.property] < self.value else self.next_operation.apply(part)

    def search_ranges(self, workflows, part):
        prop_range = part[self.property]

        result = []
        if prop_range[1] < self.value:
            if self.result_on_match == "A":
                result.append(part)
            elif self.result_on_match != "R":
                result.extend(workflows[self.result_on_match].search_ranges(workflows, part))
        elif prop_range[0] < self.value < prop_range[1]:
            r_part = copy.deepcopy(part)
            r_part[self.property] = (part[self.property][0], self.value - 1)

            l_part = copy.deepcopy(part)
            l_part[self.property] = (self.value, part[self.property][1])

            if self.result_on_match == "A":
                result.append(r_part)
            elif self.result_on_match != "R":
                result.extend(workflows[self.result_on_match].search_ranges(workflows, r_part))

            result.extend(self.next_operation.search_ranges(workflows, l_part))
        else:
            result.extend(self.next_operation.search_ranges(workflows, part))

        return result


class GreaterThan(CompareOperation):

    def apply(self, part):
        return self.result_on_match if part[self.property] > self.value else self.next_operation.apply(part)

    def search_ranges(self, workflows, part):
        prop_range = part[self.property]

        result = []
        if prop_range[0] > self.value:
            if self.result_on_match == "A":
                result.append(part)
            elif self.result_on_match != "R":
                result.extend(workflows[self.result_on_match].search_ranges(workflows, part))
        elif prop_range[1] > self.value > prop_range[0]:
            r_part = copy.deepcopy(part)
            r_part[self.property] = (part[self.property][0], self.value)

            l_part = copy.deepcopy(part)
            l_part[self.property] = (self.value + 1, part[self.property][1])

            if self.result_on_match == "A":
                result.append(l_part)
            elif self.result_on_match != "R":
                result.extend(workflows[self.result_on_match].search_ranges(workflows, l_part))

            result.extend(self.next_operation.search_ranges(workflows, r_part))
        else:
            result.extend(self.next_operation.search_ranges(workflows, part))

        return result

def parse_workflow(workflow):
    name, flow = Utils.extract_string("%{%}", workflow)

    operation = None
    for instruction in flow.split(",")[::-1]:
        if ":" in instruction:
            comparison, next_flow = instruction.split(":")
            prop = comparison[0]
            value = int(comparison[2:])
            if comparison[1] == "<":
                operation = LessThan(prop, value, next_flow, operation)
            elif comparison[1] == ">":
                operation = GreaterThan(prop, value, next_flow, operation)
            else:
                print(f"Unsupported comparison {comparison[1]}.")
        else:
            operation = Constant(instruction)

    return (name, operation)


def parse_part(part):
    return {p[0]: int(p[2:]) for p in part[1:-1].split(",")}


def solve(data):
    d_wf, d_p = data.split("\n\n")
    workflows = {workflow[0]: workflow[1] for workflow in [parse_workflow(workflow) for workflow in d_wf.split()]}
    parts = [parse_part(part) for part in d_p.split()]

    for part in parts:
        workflow_name = "in"
        while workflow_name not in ["A", "R"]:
            workflow_name = workflows[workflow_name].apply(part)
        part["result"] = workflow_name

    general_part = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    workflow_name = "in"
    ranges = workflows[workflow_name].search_ranges(workflows, general_part)

    cnt = 0
    for range in ranges:
        m = 1
        for _, value_range in range.items():
            m *= (value_range[1] - value_range[0] + 1)

        cnt += m

    return sum([sum([p[prop] for prop in p.keys() if prop != "result"])for p in parts if p["result"] == "A"]), cnt


tst_input = Utils.read_input_flat(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input_flat(f"input/day{day}_input.txt")

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
p2_tst_result = solve(tst_input)[1]
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    print("Test passed - Calculating real input now")
    p2_result = solve(puzzle_input)[1]
    submit(p2_result, part="b", day=day, year=year)
else:
    print("Test failed")
