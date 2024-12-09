import time
import Utils
from aocd import submit

day = 9
year = 2024
p1_expected_tst_result = 1928
p2_expected_tst_result = 2858

Utils.download_input(year, day)


def solve(disk_map):
    disk_size = len(disk_map)

    check_sum = 0
    p = 0

    i_ = disk_size - 1 if disk_size % 2 == 1 else disk_size - 2
    i = 0
    while i <= i_:
        if i % 2 == 0:
            file_id = int(i / 2)
            file_size = int(disk_map[i])
            check_sum += sum([file_id * (p + f_i) for f_i in range(file_size)])
            p += file_size
        else:
            free_size = int(disk_map[i])
            while free_size > 0 and i < i_:
                file_size = int(disk_map[i_])
                file_id = int(i_ / 2)

                if file_size <= free_size:
                    check_sum += sum([file_id * (p + f_i) for f_i in range(file_size)])

                    i_ -= 2
                    free_size -= file_size
                    p += file_size
                else:
                    # file_size > free_size
                    check_sum += sum([file_id * (p + f_i) for f_i in range(free_size)])

                    # i_ remains the same but we alter the disk_map
                    disk_map = disk_map[:i_] + str(file_size - free_size) + disk_map[i_ + 1:]
                    p += free_size
                    free_size = 0

        i += 1


    return check_sum


def solve2(disk_map):
    original_disk = disk_map
    disk_size = len(disk_map)

    check_sum = 0
    p = 0

    i_ = disk_size - 1 if disk_size % 2 == 1 else disk_size - 2
    i = 0
    while i < disk_size:
        if i % 2 == 0:
            file_id = int(i / 2)
            file_size = int(disk_map[i])
            check_sum += sum([file_id * (p + f_i) for f_i in range(file_size)])
            p += int(original_disk[i])
        else:
            free_size = int(disk_map[i])
            i_f = i_
            while i < i_f and free_size > 0:
                file_size = int(disk_map[i_f])
                file_id = int(i_f / 2)

                if 0 < file_size <= free_size:
                    check_sum += sum([file_id * (p + f_i) for f_i in range(file_size)])
                    disk_map = disk_map[:i_f] + "0" + disk_map[i_f + 1:]

                    free_size -= file_size
                    p += file_size

                i_f -= 2

            p += free_size

        i += 1

    return check_sum


if __name__ == "__main__":
    tst_input = Utils.read_input_flat(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input_flat(f"input/day{day}_input.txt")

    print("Part 1")
    start_time = time.time()
    p1_tst_result = solve(tst_input)
    print(f"Test solution: {p1_tst_result}.")
    elapsed_time = time.time() - start_time
    print(f"Time taken p1 test: {elapsed_time:.2f} seconds")
    if p1_tst_result == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p1_result = solve(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p1: {elapsed_time:.2f} seconds")
        submit(p1_result, part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    start_time = time.time()
    p2_tst_result = solve2(tst_input)
    elapsed_time = time.time() - start_time
    print(f"Time taken p2 test: {elapsed_time:.2f} seconds")
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        start_time = time.time()
        p2_result = solve2(puzzle_input)
        elapsed_time = time.time() - start_time
        print(f"Time taken p2: {elapsed_time:.2f} seconds")
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
