import time
import Utils
from aocd import submit

day = 22
year = 2024
p1_expected_tst_result = 37327623
p2_expected_tst_result = 23

Utils.download_input(year, day)


PRUNE_BASE = 16777216
MULTIPLICATOR = 64
DIVIDOR = 32


def prune(n):
    return n & (PRUNE_BASE - 1)  # modulo 16777216 = modulo 2^24 which is equivalent to bitwise AND 2^24 - 1. This zeroes out all bits above 2^24.


def mix(n, m):
    return n ^ m


def solve(data, loop=2000):
    secret_numbers = [int(d) for d in data]

    total = 0
    seq_m = {}
    seq_m_s = {}
    for i, n in enumerate(secret_numbers):
        p_n = n
        seq = []
        for _ in range(loop):
            m = n << 6  # multiplication by 64 = 2^6 and thus a bitshift left of 6 positions
            n = mix(n, m)
            n = prune(n)

            d = n >> 5  # division by 32 = 2^5 and thus a bitshift right of 5 positions
            n = mix(n, d)
            n = prune(n)

            m = n << 11
            n = mix(n, m)
            n = prune(n)

            # SEQ computation
            bid = (n % 10)
            seq.append(bid - (p_n % 10))
            p_n = n
            if len(seq) == 4:
                key = (seq[0], seq[1], seq[2], seq[3])
                if key not in seq_m or seq_m[key] < i:
                    seq_m[key] = i
                    if key not in seq_m_s:
                        seq_m_s[key] = bid
                    else:
                        seq_m_s[key] = seq_m_s[key] + bid
                seq.pop(0)

        total += n

    return total, max(seq_m_s.values())


if __name__ == "__main__":
    tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

    print("Part 1")
    start_time = time.time()
    p1_tst_result = solve(tst_input)[0]
    print(f"Test solution: {p1_tst_result}.")
    elapsed_time = time.time() - start_time
    print(f"Time taken p1 test: {elapsed_time:.2f} seconds")
    if p1_tst_result == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p1_result = solve(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p1: {elapsed_time:.2f} seconds")
        submit(p1_result[0], part="a", day=day, year=year)
    else:
        print("Test failed")

    tst2_input = Utils.read_input(f"input/day{day}_tst2_input.txt")
    print()
    print("Part 2")
    start_time = time.time()
    p2_tst_result = solve(tst2_input)[1]
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p2_result = p1_result[1]
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
