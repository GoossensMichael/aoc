a = ord("a")
z = ord("z")
illegal_values = (ord("i"), ord("l"), ord("o"))


def contains_double(password, ignore=" "):
    valid = False
    i = 0
    while i < len(password) - 1 and not valid:
        valid = password[i] != ignore and password[i] == password[i+1]
        i += 1

    return valid, i


def contains_two_doubles(password):
    valid, i = contains_double(password)

    return valid and contains_double(password[i+1:], password[i])[0]


def contains_straight_of_three(password):
    valid = False
    i = 0
    while i < len(password) - 3 and not valid:
        valid = password[i] + 1 == password[i + 1] and password[i + 1] + 1 == password[i + 2]
        i += 1

    return valid


def invalid(password):
    return not (contains_straight_of_three(password) and contains_two_doubles(password))


def next_legal_number(number):
    number += 1
    while number in illegal_values:
        number += 1

    return number


def increment(password):
    incremented_password = []

    # Part that introduces the increment
    # - Skip illegal values
    # - Apply overflows
    apply_increment = True
    i = len(password) - 1
    while i >= 0 and apply_increment:
        n = next_legal_number(password[i])
        if n > z:
            incremented_password.insert(0, a)
            i -= 1
        else:
            incremented_password.insert(0, n)
            i -= 1
            apply_increment = False

    # Copy rest of the password
    incremented_password = [n for n in password[0: i+1]] + incremented_password

    # If an overflow was still present then add an extra element
    if apply_increment:
        incremented_password.insert(0, a)

    return incremented_password


# The solution does not use letters but instead a list containing the ascii values of the letters.
# That way it is easy to compare and increment. At the end the numbers are translated into a string again.
def solve(password):
    proposal = increment([ord(c) for c in password])
    while invalid(proposal):
        proposal = increment(proposal)

    return "".join([chr(n) for n in proposal])


tst_input = "abcdefgh"
tst2_input = "ghjaaaaa"
puzzle_input = "vzbxkghb"

print("Part 1")
p1_test = solve(tst_input)
p1_test2 = solve(tst2_input)
print(f"Test solution: {p1_test}.")
print(f"Test 2 solution: {p1_test2}.")
p1 = ""
if p1_test == "abcdffaa" and p1_test2 == "ghjaabcc":
    p1 = solve(puzzle_input)
    print(f"Puzzle solution: {p1}.")

print()
print("Part 2")
p2_test = solve(p1_test)
p2_test2 = solve(p1_test2)
print(f"Test solution: {p2_test}.")
print(f"Test 2 solution: {p2_test2}.")
if p2_test == "abcdffbb" and p2_test2 == "ghjbbcdd":
    print(f"Puzzle solution: {solve(p1)}.")
