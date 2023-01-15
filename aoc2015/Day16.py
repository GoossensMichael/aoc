import Utils

day = 16

template = "Sue %: %: %, %: %, %: %"

ticker_tape = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}


def parse(aunt_data):
    aunts = {}
    for aunt in aunt_data:
        (aunt_number, k_1, v_1, k_2, v_2, k_3, v_3) = Utils.extract_string(template, aunt)
        aunts[int(aunt_number)] = {k_1: int(v_1), k_2: int(v_2), k_3: int(v_3)}

    return aunts


# Return False when the ticker_key is a known property of the aunt but does not correspond with the aunt
def simple_checker(ticker_key, ticker_value, aunt, aunts):
    return ticker_key in aunts[aunt] and aunts[aunt][ticker_key] != ticker_value


# Returns False if the ticker key is not a known property for the aunt
# But when it is it performs the simple checker unless it is about the properties cats, trees, goldfish or pomeranians.
# In the two first cases the value is invalid if the aunts have less or equal quantiies of the property and for the two
# latter cases the value is invalid if the aunts have greater than or equal quantities of the property.
def ranged_checker(ticker_key, ticker_value, aunt, aunts):
    if ticker_key in aunts[aunt]:
        if ticker_key in ["cats", "trees"]:
            check = aunts[aunt][ticker_key] <= ticker_value
        elif ticker_key in ["goldfish", "pomeranians"]:
            check = aunts[aunt][ticker_key] >= ticker_value
        else:
            check = simple_checker(ticker_key, ticker_value, aunt, aunts)
    else:
        check = False

    return check


def solve(aunt_data, checker):
    aunts = parse(aunt_data)

    possible_sues = []
    for aunt in aunts:
        possible = True
        i = 0
        ticker_tape_keys = [key for key in ticker_tape]
        while i < len(ticker_tape) and possible:
            ticker_key = ticker_tape_keys[i]
            ticker_value = ticker_tape[ticker_key]
            if checker(ticker_key, ticker_value, aunt, aunts):
                possible = False
            i += 1

        if possible:
            possible_sues.append(aunt)

    return possible_sues[0]


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_test = solve(tst_input, simple_checker)
print(f"Test solution: {p1_test}.")
if p1_test == 3:
    p1 = solve(puzzle_input, simple_checker)
    print(f"Puzzle solution: {p1}.")

print()
print("Part 2")
p2_test = solve(tst_input, ranged_checker)
print(f"Test solution: {p2_test}.")
if p2_test == 2:
    print(f"Puzzle solution: {solve(puzzle_input, ranged_checker)}.")
