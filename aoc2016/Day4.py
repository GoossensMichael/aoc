import Utils

day = 4


def parse(data):
    rooms = []
    for room in data:
        id_len = len(room)

        letters = {}
        room_data = room[0:id_len - 11]
        for letter in room_data:
            if letter != '-' and letter not in letters:
                letters[letter] = room_data.count(letter)

        count_by_letter = sorted([(letter, letters[letter]) for letter in letters], key=lambda e: (-1 * e[1], e[0]))
        # Tuple structure: (map of occurrence by letter, sector_id, checksum, encoded_string)
        rooms.append((count_by_letter, int(room[id_len - 10:id_len - 7]), room[id_len - 6:id_len - 1], room_data))

    return rooms


def is_real_room(room):
    if len(room[0]) < 5:
        return False
    else:
        return "".join([room[0][i][0] for i in range(5)]) == room[2]


def solve(data):
    sector_sum = 0
    real_rooms = []
    for room in parse(data):
        if is_real_room(room):
            sector_sum += room[1]
            real_rooms.append(room)

    return sector_sum, real_rooms


def decrypt(rooms):
    decrypted_rooms = {}
    for room in rooms:
        decrypted_room = ""
        for letter in room[3]:
            if letter == "-":
                decrypted_room += " "
            else:
                decrypted_room += chr(((ord(letter) - 97 + room[1]) % 26) + 97)
            decrypted_rooms[decrypted_room] = room[1]

    return decrypted_rooms


tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")

print("Part 1")
p1_test = solve(tst_input)
print(f"Test solution: {p1_test[0]}.")
p1 = []
if p1_test[0] == 1857:
    p1 = solve(puzzle_input)
    print(f"Puzzle solution: {p1[0]}.")

print()
print("Part 2")
p2_test = decrypt(p1_test[1])["very encrypted name"]
print(f"Test solution: {p2_test}.")
if p2_test == 343:
    p2 = decrypt(p1[1])["northpole object storage"]
    print(f"Puzzle solution: {p2}.")
