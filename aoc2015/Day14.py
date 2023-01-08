import Utils

day = 14

template = "% can fly % km/s for % seconds, but then must rest for % seconds."


def parse(data):
    # Returns (name, speed, flight_time, rest_time)
    return [Utils.extract_string(template, reindeer_stats) for reindeer_stats in data]


def solve(data, duration):
    reindeer_stats = parse(data)

    results = []
    max_distance = 0
    for reindeer_stat in reindeer_stats:
        (name, speed, flying_time, resting_time) = (reindeer_stat[0],
                                                    int(reindeer_stat[1]),
                                                    int(reindeer_stat[2]),
                                                    int(reindeer_stat[3]))

        cycle = flying_time + resting_time
        distance = ((duration // cycle) * speed * flying_time) + (min((duration % cycle), flying_time) * speed)
        results.append((name, distance))
        if distance > max_distance:
            max_distance = distance

    # Find the max_distance distance
    return max_distance


def solve_p2(data, duration):
    reindeer_stats = parse(data)

    reindeer_scores = {}
    reindeer_states = init_reindeer_states(reindeer_scores, reindeer_stats)

    first_reindeer = reindeer_states[0]["name"]
    for _ in range(duration):
        for reindeer in reindeer_states:
            reindeer_name = reindeer["name"]
            if reindeer["remaining_resting_time"] > 0:
                reindeer["remaining_resting_time"] -= 1
            else:
                if reindeer["flight_time"] + 1 >= reindeer["flying_time"]:
                    reindeer["flight_time"] = 0
                    reindeer["remaining_resting_time"] = reindeer["resting_time"]
                else:
                    reindeer["flight_time"] += 1
                reindeer_scores[reindeer_name] = (reindeer_scores[reindeer_name][0] + reindeer["speed"],
                                                  reindeer_scores[reindeer_name][1])

            if reindeer_scores[first_reindeer][0] < reindeer_scores[reindeer_name][0]:
                first_reindeer = reindeer_name

        update_score(first_reindeer, reindeer_scores, reindeer_states)

    return reindeer_scores[first_reindeer][0], determine_high_score(reindeer_scores)


def init_reindeer_states(reindeer_scores, reindeer_stats):
    reindeer_states = []
    for reindeer_stat in reindeer_stats:
        reindeer_states.append({
            "name": reindeer_stat[0], "speed": int(reindeer_stat[1]), "flying_time": int(reindeer_stat[2]),
            "resting_time": int(reindeer_stat[3]), "flight_time": 0, "remaining_resting_time": 0, "distance": 0,
            "points": 0})
        reindeer_scores[reindeer_stat[0]] = (0, 0)

    return reindeer_states


def update_score(first_reindeer, reindeer_scores, reindeer_states):
    for reindeer in reindeer_states:
        reindeer_name = reindeer["name"]
        if reindeer_scores[reindeer_name][0] == reindeer_scores[first_reindeer][0]:
            reindeer_scores[reindeer_name] = (reindeer_scores[reindeer_name][0], reindeer_scores[reindeer_name][1] + 1)


def determine_high_score(reindeer_scores):
    high_score = 0
    for name in reindeer_scores:
        if reindeer_scores[name][1] > high_score:
            high_score = reindeer_scores[name][1]
    return high_score


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_test = solve(tst_input, 1000)
print(f"Test solution: {p1_test}.")
p1_test2 = solve_p2(tst_input, 1000)
print(f"Test solution with p2 solver: (distance = {p1_test2[0]}, score = {p1_test2[1]}).")
if p1_test == 1120:
    p1 = solve(puzzle_input, 2503)
    print(f"Puzzle solution: {p1}.")
    p1_2 = solve_p2(puzzle_input, 2503)
    print(f"Puzzle solution with p2 solver: (distance = {p1_2[0]}, score = {p1_2[1]}).")

print()
print("Part 2")
p2_test = solve_p2(tst_input, 1000)
print(f"Test solution: (distance = {p2_test[0]}, score = {p2_test[1]}).")
if p2_test[1] == 689:
    print(f"Puzzle solution: {solve_p2(puzzle_input, 2503)[1]}.")
