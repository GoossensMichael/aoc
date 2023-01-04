def read_input(file_name):
    f = None
    try:
        f = open(file_name, "r")
        return [line[:-1] if line[-1] == "\n" else line for line in f]
    except IOError:
        print("Error while performing io operations.")
    finally:
        if f is not None:
            f.close()


def decode(line):
    i = 1
    new_line = ""
    while i < len(line) - 1:
        if line[i] == "\\":
            next_char = line[i+1]
            if next_char == "\\" or next_char == "\"":
                new_line += line[i+1]
                i += 2
            elif next_char == "x":
                new_line += chr(int(line[i+2:i+4], 16))
                i += 4
            else:
                raise Exception("Did not expect character " + next_char + " after character " + line[i] + " which is character " + str(i) + ".")
        else:
            new_line += line[i]
            i += 1

    return new_line


def encode(line):
    i = 0
    new_line = "\""
    while i < len(line):
        if line[i] == "\"":
            new_line += "\\\""
        elif line[i] == "\\":
            new_line += "\\\\"
        else:
            new_line += line[i]
        i += 1

    new_line += "\""

    print(f"{line} - {len(line)} vs {len(new_line)} - {new_line}")
    return new_line


def solve(lines, transformation):
    count = 0
    for line in lines:
        count += abs(len(line) - len(transformation(line)))

    return count


tst_input = read_input("input/day8_tst_input.txt")
puzzle_input = read_input("input/day8_input.txt")

print("Part 1")
print(f"Test input: {solve(tst_input, decode)}.")
print(f"Puzzle input: {solve(puzzle_input, decode)}.")

print()
print("Part 2")
print(f"Test input: {solve(tst_input, encode)}.")
print(f"Puzzle input: {solve(puzzle_input, encode)}.")
