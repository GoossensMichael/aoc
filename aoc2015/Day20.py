import Utils
from math import sqrt
from functools import reduce
from aocd import submit

day = 20
year = 2015
p1_expected_tst_result = 8
p2_expected_tst_result = 8

Utils.download_input(year, day)


def prime_factors(n):
    '''lists prime factors, from greatest to smallest'''
    i = 2
    while i<=sqrt(n):
        if n%i==0:
            l = prime_factors(n / i)
            l.append(i)
            return l
        i+=1
    return [n]


def factor_generator(n):
    p = prime_factors(n)
    factors = {}
    for p1 in p:
        try:
            factors[p1] += 1
        except KeyError:
            factors[p1] = 1
    return factors


def divisor_gen(n):
    factors = [(f, m) for f, m in factor_generator(n).items()]
    nfactors = len(factors)
    f = [0] * nfactors
    while True:
        yield reduce(lambda x, y: x*y, [factors[x][0]**f[x] for x in range(nfactors)], 1)
        i = 0
        while True:
            f[i] += 1
            if f[i] <= factors[i][1]:
                break
            f[i] = 0
            i += 1
            if i >= nfactors:
                return


# Calculate alle divisors of a number. Then add them all together.
# Don't multiply by 10, then the input can also be reduced 10 times.
def solve(data):
    target = int(data[0])/10
    house_number = 1

    while sum([e for e in divisor_gen(house_number)]) < target:
        house_number += 1

    return house_number


def solve_p2(data):
    target = int(data[0])
    house_number = 1

    elves = {}
    score = 0
    while score < target:
        score = 0
        for visitor_elve in divisor_gen(house_number):
            if visitor_elve not in elves:
                elves[visitor_elve] = 0

            if elves[visitor_elve] < 50:
                score += visitor_elve * 11
                elves[visitor_elve] += 1

        house_number += 1

    return house_number - 1


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
