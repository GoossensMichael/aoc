import hashlib

def solve(secret, expected_prefix):
    n = 1
    while not str(hashlib.md5(str.encode(secret + str(n))).hexdigest()).startswith(expected_prefix):
        n += 1
    print(n)


tst_input = "abcdef"

input = "bgvyzdsv"

solve(tst_input, "00000")
solve(input, "00000")

solve(tst_input, "000000")
solve(input, "000000")

