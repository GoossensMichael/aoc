import math
import Utils

day = 15

template = "%: capacity %, durability %, flavor %, texture %, calories %"


def permutate(base, used, max, times, results):
    if times > 1:
        for i in range(1, max):
            if (used + i < max):
                new_base = list(base)
                new_base.append(i)
                permutate(new_base, used + i, max, times - 1, results)
    else:
        new_base = list(base)
        new_base.append(max - used)
        results.append(new_base)


def solve(data):
    ingredients = [Utils.extract_string(template, d) for d in data]

    amt_of_ingredients = len(ingredients)
    amt_of_properties = len(ingredients[0][1:-1])

    permutations = []
    permutate([], 0, 100, amt_of_ingredients, permutations)

    highest_score = 0
    for permutation in permutations:
        property_scores = [0 for _ in range(amt_of_properties)]
        for i_i in range(amt_of_ingredients):
            for p_i in range(amt_of_properties):
                property_scores[p_i] += permutation[i_i] * int(ingredients[i_i][p_i + 1])

        score = math.prod([0 if p_s < 0 else p_s for p_s in property_scores])

        if score > highest_score:
            highest_score = score

    return highest_score


def solve_p2(data):
    ingredients = [Utils.extract_string(template, d) for d in data]

    amt_of_ingredients = len(ingredients)
    amt_of_properties = len(ingredients[0][1:])

    permutations = []
    permutate([], 0, 100, amt_of_ingredients, permutations)

    highest_score = 0
    for permutation in permutations:
        property_scores = [0 for _ in range(amt_of_properties)]
        for i_i in range(amt_of_ingredients):
            for p_i in range(amt_of_properties):
                property_scores[p_i] += permutation[i_i] * int(ingredients[i_i][p_i + 1])

        if property_scores[-1] == 500:
            score = math.prod([0 if p_s < 0 else p_s for p_s in property_scores[:-1]])

            if score > highest_score:
                highest_score = score

    return highest_score


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_test = solve(tst_input)
print(f"Test solution: {p1_test}.")
if p1_test == 62842880:
    p1 = solve(puzzle_input)
    print(f"Puzzle solution: {p1}.")

print()
print("Part 2")
p2_test = solve_p2(tst_input)
print(f"Test solution: {p2_test}.")
if p2_test == 57600000:
    print(f"Puzzle solution: {solve_p2(puzzle_input)}.")
