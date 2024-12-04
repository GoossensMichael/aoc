import Utils
from aocd import submit

day = 21
year = 2015
p1_expected_tst_result = 0
p2_expected_tst_result = 0

Utils.download_input(year, day)


def parse(shop_data):
    (w_d, a_d, r_d) = shop_data[1:].split("\n\n")

    return { "weapons": parse_items(w_d), "armor": parse_items(a_d), "rings": parse_rings(r_d)}


def parse_rings(r_d):
    return [(f"{a[0]} {a[1]}", int(a[2]), int(a[3]), int(a[4])) for a in
            [a.split() for a in r_d.split("\n")[1:] if a != ""]]


def parse_items(d):
    return [(a[0], int(a[1]), int(a[2]), int(a[3])) for a in [a.split() for a in d.split("\n")[1:]]]


def fight(boss, hero):
    while boss["Hit Points"] > 0 and hero["Hit Points"] > 0:
        boss["Hit Points"] = max(boss["Hit Points"] - damage(boss, hero), 0)

        if boss["Hit Points"] > 0:
            hero["Hit Points"] = max(hero["Hit Points"] - damage(hero, boss), 0)

    return hero["Hit Points"] > 0

def damage(boss, hero):
    return max(boss["Armor"] - hero["damage"], 1)


def solve(data, shop_data):
    shop = parse(shop_data)

    # Get all permutations from item shop
    # Simulate fight. If win return the gold. Get the min of all fights.

    return 0

shop = Utils.read_input_flat(f"input/day{day}_shop_input.txt")
tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_tst_result = solve(tst_input, shop)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    p1_result = solve(puzzle_input, shop)
    print(f"Puzzle solution: {p1_result}.")
    if input("submit part 1? (y or n) - ") == "y":
        submit(p1_result, part="a", day=day, year=year)

print()
print("Part 2")
p2_tst_result = solve(tst_input)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    p2_result = solve(puzzle_input)
    print(f"Puzzle solution: {p2_result}.")
    if input("submit part 2? (y or n) - ") == "y":
        submit(p2_result, part="b", day=day, year=year)
