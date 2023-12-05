from difflib import SequenceMatcher
import aocd
import os


def download_input(year, day):
    file_name = f"input/day{day}_input.txt"
    if os.path.exists(file_name):
        print(f"Input file {file_name} already exists, skipping download.")
    else:
        print(f"Downloading input file {file_name}.")
        open(file_name, 'w').write(aocd.get_data(year=year, day=day))


def read_input_flat(file_name):
    f = None
    try:
        f = open(file_name, "r")

        content = ""
        for line in f:
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
    seq = SequenceMatcher(None, template, text, True)
    return [text[c:d] for tag, a, b, c, d in seq.get_opcodes() if tag == 'replace']
