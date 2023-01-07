import Utils

day = 13

template = "% would % % happiness units by sitting next to %."


def parse(data):
    preferences = [Utils.extract_string(template, text) for text in data]
    preferences_by_name = dict()

    for (name, sentiment, happiness, neighbour) in preferences:
        preferences_for_name = preferences_by_name.get(name, {})
        preferences_for_name[neighbour] = (int(happiness) if sentiment == "gain" else -1 * int(happiness))
        preferences_by_name[name] = preferences_for_name

    return preferences_by_name


def permutate(names, permutations):
    if len(names) == len(permutations[0]):
        return permutations
    else:
        new_permutations = []
        for permutation in permutations:
            unused_names = [name for name in names if name not in permutation ]
            for unused_name in unused_names:
                new_permutation = list(permutation)
                new_permutation.append(unused_name)
                new_permutations.append(new_permutation)
        return permutate(names, new_permutations)


def calculate_happiness(preferences_by_name, permutation, i):
    preference_for_name = preferences_by_name[permutation[i]]

    after = (i + 1) % len(permutation)
    before = len(permutation) - 1 if i == 0 else i - 1
    return preference_for_name[permutation[before]] + preference_for_name[permutation[after]]


def add_ambivalent_person(preferences_by_name):
    ambivalent = "ambivalent"
    preferences_by_name[ambivalent] = {}

    for name in preferences_by_name:
        preferences_by_name[name][ambivalent] = 0
        preferences_by_name[ambivalent][name] = 0


def solve(data, add_self=False):
    preferences_by_name = parse(data)
    if add_self:
        add_ambivalent_person(preferences_by_name)

    names = [name for name in preferences_by_name.keys()]

    permutations = permutate(set(names), [[names[0]]])
    results = []
    greatest_happiness = 0
    for permutation in permutations:
        happiness = 0
        for i in range(len(permutation)):
            happiness += calculate_happiness(preferences_by_name, permutation, i)

        results.append((permutation, happiness))
        if greatest_happiness < happiness:
            greatest_happiness = happiness

    return greatest_happiness


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_test = solve(tst_input)
print(f"Test solution: {p1_test}.")
if p1_test == 330:
    p1 = solve(puzzle_input)
    print(f"Puzzle solution: {p1}.")

print()
print("Part 2")
p2_test = solve(tst_input, True)
print(f"Test solution: {p2_test}.")
if p2_test == 286:
    print(f"Puzzle solution: {solve(puzzle_input, True)}.")
