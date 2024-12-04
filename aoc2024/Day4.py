import Utils
from aocd import submit

day = 4
year = 2024
p1_expected_tst_result = 18
p2_expected_tst_result = 9

Utils.download_input(year, day)

word = "XMAS"
word_len = len(word)

cross_patterns = [
    ("S", "M", "S", "M"),  # Original
    ("M", "S", "M", "S"),  # Rotated
    ("M", "M", "S", "S"),  # Flipped
    ("S", "S", "M", "M"),  # Flipped reverse
]


def parse(data):
    return [list(row) for row in data]


def find_word(x, y, dx, dy, grid):
    rows = len(grid)
    cols = len(grid[0])

    for i in range(word_len):
        nx, ny = x + i * dx, y + i * dy
        if not (0 <= nx < rows and 0 <= ny < cols) or grid[nx][ny] != word[i]:
            return False
    return True


def solve(data):
    grid = parse(data)

    # Dimensions
    rows = len(grid)
    cols = len(grid[0])

    # Directions for traversal
    directions = [
        (0, 1),  # left to right
        (0, -1),  # right to left
        (1, 0),  # top to bottom
        (-1, 0),  # bottom to top
        (1, 1),  # diagonal down-right
        (-1, -1),  # diagonal up-left
        (1, -1),  # diagonal down-left
        (-1, 1),  # diagonal up-right
    ]

    found_positions = []

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == word[0]:  # Match first letter
                for dx, dy in directions:
                    if find_word(row, col, dx, dy, grid):
                        found_positions.append(((row, col), (dx, dy)))

    return len(found_positions)


def check_cross(x, y, pattern, table):
    upleft, upright, downleft, downright = pattern
    # Ensure bounds and match the pattern
    return (table[x][y] == "A" and       # Center
            table[x - 1][y - 1] == upleft and    # Up
            table[x - 1][y + 1] == upright and  # Down
            table[x + 1][y - 1] == downleft and  # Left
            table[x + 1][y + 1] == downright     # Right
            )


def solve2(data):
    grid = parse(data)

    cross_positions = []

    # Dimensions
    rows = len(grid)
    cols = len(grid[0])

    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            for pattern in cross_patterns:
                if check_cross(row, col, pattern, grid):
                    cross_positions.append((row, col, pattern))

    return len(cross_positions)

if __name__ == "__main__":
    tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
    puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

    print("Part 1")
    p1_tst_result = solve(tst_input)
    print(f"Test solution: {p1_tst_result}.")
    if p1_tst_result == p1_expected_tst_result:
        print("Test passed - Calculating real input now")
        p1_result = solve(puzzle_input)
        submit(p1_result, part="a", day=day, year=year)
    else:
        print("Test failed")

    print()
    print("Part 2")
    p2_tst_result = solve2(tst_input)
    print(f"Test solution: {p2_tst_result}.")
    if p2_tst_result == p2_expected_tst_result:
        print("Test passed - Calculating real input now")
        p2_result = solve2(puzzle_input)
        submit(p2_result, part="b", day=day, year=year)
    else:
        print("Test failed")
