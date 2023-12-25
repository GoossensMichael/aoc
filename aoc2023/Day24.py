import itertools

from aocd import submit

import Utils

day = 24
year = 2023
p1_expected_tst_result = 2
p2_expected_tst_result = 47

Utils.download_input(year, day)


def within_limit(v, limit):
    return limit[0] <= v <= limit[1]


def to_linear_equation(x, y, vx, vy):
    return vy / vx, y - (x * vy) / vx


def solve(data, limit):
    hail_storm = [Utils.extract_int("%, %, % @ %, %, %", d) for d in data]

    cnt = 0
    while len(hail_storm) > 0:
        (x, y, z, vx, vy, vz) = hail_storm.pop(0)

        for (x_, y_, z_, vx_, vy_, vz_) in hail_storm:
            l1 = to_linear_equation(x, y, vx, vy)
            l2 = to_linear_equation(x_, y_, vx_, vy_)

            if l1[0] == l2[0]:
                i_x = None
            else:
                i_x = (l2[1] - l1[1]) / (l1[0] - l2[0])

            if i_x is not None:
                i_y = l1[0] * i_x + l1[1]
                tx = (i_x - x) / vx
                ty = (i_x - x_) / vx_
                if tx >= 0 and ty >= 0 and within_limit(i_x, limit) and within_limit(i_y, limit):
                    cnt += 1

    return cnt


def calculate_intersection_value(a, b, c, d, p, q, r, s):
    # det = AD - BC
    # ( A = c - a, B = r - p )
    # ( C = d - b, D = s - q )
    det = (c - a) * (s - q) - (r - p) * (d - b)

    # Lines are parallel
    if det == 0:
        return None

    # Calculate intersection value
    return round(((s - q) * (r - a) + (p - r) * (s - b)) / det)


def find_intersection_point(l, r, dim_1, dim_2):
    intersection_value = calculate_intersection_value(
        l[dim_1], l[dim_2], l[dim_1] + l[dim_1 + 3], l[dim_2] + l[dim_2 + 3],
        r[dim_1], r[dim_2], r[dim_1] + r[dim_1 + 3], r[dim_2] + r[dim_2 + 3])

    # No intersection
    if intersection_value is None:
        return None

    # Apply intersection value to the velocities to get the actual coordinates.
    return (l[dim_1] + intersection_value * l[dim_1 + 3], l[dim_2] + intersection_value * l[dim_2 + 3])


def find_common_intersection(v, dim_1, dim_2, hail_storm):
    intersection = None

    # Copy the hailstorm and adjust the velocities of the two provided dimensions.
    velocity_applied = [
        [p + v[0] if i == dim_1 + 3 else p + v[1] if i == dim_2 + 3 else p for i, p in enumerate(hail)]
        for hail in hail_storm
    ]

    for l, r in itertools.combinations(velocity_applied, 2):
        n_intersection = find_intersection_point(l, r, dim_1, dim_2)
        if n_intersection is not None:
            if intersection is None:
                intersection = n_intersection
            if not (n_intersection[0] == intersection[0] and n_intersection[1] == intersection[1]):
                # When not all intersection points are the same return false.
                return False

    return intersection


def solve_p2(data):
    hail_storm = [Utils.extract_int("%, %, % @ %, %, %", d) for d in data]

    limited_hail_storm = hail_storm[:5]

    # Loop over all x and y values
    for x in range(int(1e18)):
        for y in range(x + 1):
            # Look both forwards and backwards in each direction
            for d_x, d_y in [[1, 1], [1, -1], [-1, 1], [-1, -1]]:

                xy = find_common_intersection([x * d_x, y * d_y], 0, 1, limited_hail_storm)
                if xy:
                    # Search on z axis as well
                    for z in range(int(1e18)):
                        # Also in both directions
                        for sz in [1, -1]:
                            xz = find_common_intersection([x * d_x, z * sz], 0, 2, limited_hail_storm)
                            if xz:
                                return xy[0] + xy[1] + xz[1]


if __name__ == "__main__":
    tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

    test_area = [7, 27]
    puzzle_area = [200_000_000_000_000, 400_000_000_000_000]
    print("Part 1")
    p1_tst_result = solve(tst_input, test_area)
    print(f"Test solution: {p1_tst_result}.")
    if p1_tst_result == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        p1_result = solve(puzzle_input, puzzle_area)
        submit(p1_result, part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    p2_tst_result = solve_p2(tst_input)
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        p2_result = solve_p2(puzzle_input)
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
