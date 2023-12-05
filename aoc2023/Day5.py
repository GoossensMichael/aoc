import Utils
from aocd import submit

day = 5
year = 2023
p1_expected_tst_result = 35
p2_expected_tst_result = 46

Utils.download_input(year, day)


def parse_block(block):
    block_lines = block.split("\n")
    f, t = Utils.extract_string("%-to-% map", block_lines[0])

    return {
        "from": f,
        "to": t,
        "mappings": [{"destination": m[0], "source": m[1], "range": m[2]} for m in [[int(n) for n in l.split()] for l in block_lines[1:] if l != ""]]
    }


def parse(data, seeds_are_ranges):
    blocks = data.split("\n\n")

    seeds_block = blocks[0].split(" ")
    result = {"seeds": [int(seed) for seed in seeds_block[1:]], "transitions": {}}
    for i in range(1, len(blocks)):
        block = parse_block(blocks[i])
        result["transitions"][block["from"]] = block

    if seeds_are_ranges:
        result["seeds"] = [(a, a + b - 1) for a, b in zip(result["seeds"][::2], result["seeds"][1::2])]
    else:
        result["seeds"] = [(seed, seed) for seed in result["seeds"]]

    return result


def source_to_destination(t, value):
    mapping = next((mapping for mapping in t["mappings"] if
                    value in range(mapping["source"], mapping["source"] + mapping["range"])), None)
    if mapping:
        new_value = value + mapping["destination"] - mapping["source"]
    else:
        new_value = value

    return new_value


def calculate_ranges(r, mappings):
    if mappings:
        sorted_mappings = sorted(mappings, key = lambda x: x["source"])
        new_ranges = []

        current = r[0]
        for m in sorted_mappings:
            if current < m["source"]:
                new_ranges.append((current, m["source"] - 1))
                current = m["source"]

            m_bound = m["source"] + m["range"]
            new_ranges.append((current, min(m_bound - 1, r[1])))
            current = m_bound

        if current < r[1]:
            new_ranges.append((current, r[1]))

    else:
        new_ranges = [r]

    return new_ranges


def transition(almanac, ranges, target_category, current_category="seed"):
    if current_category == target_category:
        return ranges
    else:
        new_ranges = []
        t = almanac["transitions"][current_category]
        for r in ranges:
            mappings = [m for m in t["mappings"] if m["source"] + m["range"] > r[0] and m["source"] <= r[1]]
            new_ranges.extend([(source_to_destination(t, nr[0]), source_to_destination(t, nr[1])) for nr in calculate_ranges(r, mappings)])

        return transition(almanac, new_ranges, target_category, t["to"])


def solve(data, seeds_are_ranges=False):
    almanac = parse(data, seeds_are_ranges)

    locations = []
    for seed in almanac["seeds"]:
        locations.extend(transition(almanac, [seed], "location"))

    return min([l[0] for l in locations])


tst_input = Utils.read_input_flat(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input_flat(f"input/day{day}_input.txt")

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
p2_tst_result = solve(tst_input, True)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    p2_result = solve(puzzle_input, True)
    print(f"Puzzle solution: {p2_result}.")
    if input("submit part 2? (y or n) - ") == "y":
        submit(p2_result, part="b", day=day, year=year)
