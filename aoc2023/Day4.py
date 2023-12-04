import Utils
from aocd import submit

day = 4
year = 2023
p1_expected_tst_result = 13
p2_expected_tst_result = 30

Utils.download_input(year, day)

template = "Card %: % | %"


def solve(data):
    cards = parse(data)

    total_points = 0
    for card in cards:
        points = 0
        for winning_number in card[1]:
            if winning_number in card[2]:
                points = 1 if points == 0 else points * 2
        total_points += points

    return total_points


def solve_p2_naive(data):
    cards = parse(data)
    cache = dict()

    i = 0
    while i < len(cards):
        card = cards[i]
        i += 1

        score = cache.get(card[0]) if card[0] in cache else sum([1 for n in card[1] if n in card[2]])
        cards.extend([cards[ci] for ci in range(card[0], card[0] + score)])

    return len(cards)


def solve_p2(data):
    cards = [{"cnt": 1, "card_id": a, "winning_numbers": b, "my_numbers": c} for a, b, c in parse(data)]

    for card in cards:
        for i in range(card["card_id"], card["card_id"] + len(card["winning_numbers"].intersection(card["my_numbers"]))):
            cards[i]["cnt"] += card["cnt"]

    return sum([card["cnt"] for card in cards])


def parse(data):
    return [(int(c[0]), set([int(n) for n in c[1].split()]), set([int(n) for n in c[2].split()])) for c in [Utils.extract_string(template, d) for d in data]]


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    p1_result = solve(puzzle_input)
    print(f"Puzzle solution: {p1_result}.")
    if input("submit part 1? (y or n) - ") == "y":
        submit(p1_result, part="a", day=day, year=year)

print()
print("Part 2")
p2_tst_result = solve_p2(tst_input)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    p2_result = solve_p2(puzzle_input)
    print(f"Puzzle solution: {p2_result}.")
    if input("submit part 2? (y or n) - ") == "y":
        submit(p2_result, part="b", day=day, year=year)
