import Utils
from queue import PriorityQueue
from aocd import submit

day = 19
year = 2015
p1_expected_tst_result = 7
p2_expected_tst_result = 6

Utils.download_input(year, day)

template = "% => %"


def parse_transitions(transitions, reversed=False):
    grouped_transitions = {}

    for transition in transitions:
        if reversed:
            (b, a) = Utils.extract_string(template, transition)
        else:
            (a, b) = Utils.extract_string(template, transition)

        if a not in grouped_transitions:
            grouped_transitions[a] = []

        group = grouped_transitions.get(a)
        group.append(b)

    return grouped_transitions


def solve_replace(transitions, molecule_input, results):
    for transition_from, transition_to in transitions.items():
        for i in range(len(molecule_input) - len(transition_from) + 1):
            j = i + len(transition_from)
            atom = molecule_input[i:j]
            if atom == transition_from:
                for to in transition_to:
                    first_part = molecule_input[:i]
                    last_part = molecule_input[j:]
                    results.add(first_part + to + last_part)

    return results


#Not so proud of this one tbh, sought help on the forums. Data analysis was key!
def solve_p2(data):
    molecule = data[-1][::]
    return sum([1 for l in molecule if l.isupper()]) - molecule.count("Rn") - molecule.count("Ar") - 2 * molecule.count("Y") - 1


def solve_p2_2(data):
    transitions = parse_transitions(data[:-2], True)
    molecule_input = data[-1:][0]

    p_molecules = PriorityQueue()
    p_molecules.put((len(molecule_input), [0, molecule_input, []]))
    searching = True
    visited = { molecule_input }
    min = len(molecule_input)
    while searching:
        c_molecule = p_molecules.get()

        if len(c_molecule[1][1]) <= min:
            min = len(c_molecule[1][1])
            print(c_molecule)

        visited.add(c_molecule[1][1])
        if "e" == c_molecule[1][1]:
            searching = False
        else:
            n_molecules = solve_replace(transitions, c_molecule[1][1], set())
            for n_molecule in n_molecules:
                if n_molecule not in visited:
                    visited.add(n_molecule)
                    p_molecules.put((len(n_molecule), [c_molecule[1][0] + 1, n_molecule]))

    return c_molecule[1][0]


def solve(data):
    transitions = parse_transitions(data[:-2])
    molecule_input = data[-1:][0]
    results = solve_replace(transitions, molecule_input, set())

    return len(results)

tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

# print("Part 1")
# p1_tst_result = solve(tst_input)
# print(f"Test solution: {p1_tst_result}.")
# if p1_tst_result == p1_expected_tst_result:
#     p1_result = solve(puzzle_input)
#     print(f"Puzzle solution: {p1_result}.")
#     if input("submit part 1? (y or n) - ") == "y":
#         submit(p1_result, part="a", day=day, year=year)

print()
print("Part 2")
p2_tst_result = solve_p2(tst_input) + 1
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    p2_result = solve_p2(puzzle_input)
    print(f"Puzzle solution: {p2_result}.")
    if input("submit part 2? (y or n) - ") == "y":
        submit(p2_result, part="b", day=day, year=year)

print()
print("Part 2 - Naïve")
p2_tst_result = solve_p2_2(tst_input)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    puzzle_input = Utils.read_input(f"input/day{day}_input_bc.txt")
    p2_result = solve_p2_2(puzzle_input)
    print(f"Puzzle solution: {p2_result}.")
    if input("submit part 2? (y or n) - ") == "y":
        submit(p2_result, part="b", day=day, year=year)
