from difflib import SequenceMatcher
import aocd
import os
import re


def download_input(year, day):
    file_name = f"input/day{day}_input.txt"
    if os.path.exists(file_name):
        print(f"Input file {file_name} already exists, skipping download.")
    else:
        print(f"Downloading input file {file_name}.")
        open(file_name, 'w').write(aocd.get_data(year=year, day=day))


def tiles(data):
    return [[t for t in l] for l in data]


def tiles_int(data):
    return [[int(t) for t in l] for l in data]


def add_2d(a_2d, b_2d):
    return a_2d[0] + b_2d[0], a_2d[1] + b_2d[1]

def coord_valid(coord, m):
    return 0 <= coord[0] < len(m) and 0 <= coord[1] < len(m[0])


def rotate90(coord):
    return -coord[1], coord[0]


def rotate_min_90(coord):
    return coord[1], -coord[0]


def rotate(coord, deg):
    if deg == 90:
        return rotate90(coord)
    elif deg == -90:
        return rotate_min_90(coord)
    elif deg == 0:
        return coord
    else:
        raise ValueError("Only supporting rotations 0, 90 and -90")


def at_coord(m, coord):
    return m[coord[0]][coord[1]]


def read_input_flat(file_name):
    f = None
    try:
        f = open(file_name, "r")

        content = ""
        for line in f:
            if line != "":
                content += line

        return content
    except IOError:
        print("Error while performing io operations.")
    finally:
        if f is not None:
            f.close()


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


# Extract template variables from a text as integers.
# For example template: "toggle %,% through %,%"
#                 text: "toggle 239,400 through 100,199"
# Then to recover 239, 400, 100 and 199 as variables write the following code:
#
# w, x, y, z = extract("toggle %,% through %,%", "toggle 239,400 through 100,199")
def extract_int(template, text):
    seq = SequenceMatcher(None, template, text, True)
    return [int(text[c:d]) for tag, a, b, c, d in seq.get_opcodes() if tag == 'replace']


# Same as above but the resulting variables are strings.
def extract_string(template, text):
    # Escape special characters
    escaped_template = re.escape(template)
    escaped_text = re.escape(text)

    # Create SequenceMatcher
    seq = SequenceMatcher(None, escaped_template, escaped_text, True)

    # Extract replaced substrings
    return [escaped_text[c:d] for tag, a, b, c, d in seq.get_opcodes() if tag == 'replace']

# Print
def print_map(m):
    for x in range(len(m)):
        l = ""
        for y in range(len(m[x])):
            l += m[x][y]
        print(l)
    print()

def print_map_points(points):
    max_x = max([x for x, y in points])
    min_x = min([x for x, y in points])
    max_y = max([y for x, y in points])
    min_y = min([y for x, y in points])

    for x in range(min_x, max_x + 1):
        l = ""
        for y in range(min_x, max_y + 1):
            if (x, y) in points:
                l += "#"
            else:
                l += "."
        print(l)
    print()
