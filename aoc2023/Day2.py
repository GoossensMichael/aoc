import Utils
from aocd import submit

day = 2
year = 2023
p1_expected_tst_result = 8
p2_expected_tst_result = 2286

Utils.download_input(year, day)

def is_good_pull(pull):
    for color in pull:
        if cubes[color[1]] < int(color[0]):
            return False
    return True

def is_good_game(pulls):
    for pull in pulls:
        if not is_good_pull(pull):
            return False

    return True

def parse_games(data):
    return [
        {
            "game_id": int(game[0]),
            "pulls": [list(map(str.split, pull.split(", "))) for pull in game[1].split("; ")]
        }
        for game in (Utils.extract_string("Game %: %", line) for line in data)
    ]

def solve(data):
    return sum(game['game_id'] for game in parse_games(data) if is_good_game(game['pulls']))

def solve2(data):
    games = parse_games(data)

    total = 0
    for game in games:
        minimum_cubes = {"red": 0, "green": 0, "blue": 0}
        for pull in game["pulls"]:
            for color in pull:
                if int(color[0]) > minimum_cubes[color[1]]:
                    minimum_cubes[color[1]] = int(color[0])

        total += minimum_cubes["red"] * minimum_cubes["green"] * minimum_cubes["blue"]

    return total

tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

cubes = {
    "red": 12,
    "green": 13,
    "blue": 14
}

print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    p1_result = solve(puzzle_input)
    print(f"Puzzle solution: {p1_result}.")
    if (input("submit part 1? (y or n) - ") == "y"):
        submit(p1_result, part="a", day=day, year=year)

print()
print("Part 2")
p2_tst_result = solve2(tst_input)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    p2_result = solve2(puzzle_input)
    print(f"Puzzle solution: {p2_result}.")
    if (input("submit part 2? (y or n) - ") == "y"):
        submit(p2_result, part="b", day=day, year=year)
