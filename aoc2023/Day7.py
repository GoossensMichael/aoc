import operator as op
import Utils
from aocd import submit

day = 7
year = 2023
p1_expected_tst_result = 6440
p2_expected_tst_result = 5905

Utils.download_input(year, day)


FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1
STRENGTHS = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}


def group_cards(cards, increase_largest_group):
    grouped_cards = {}
    for card in cards:
        grouped_cards[card] = op.countOf(cards, card)

    sorted_grouped_cards = sorted(grouped_cards.values(), reverse=True)
    # The code below should be removed when using the readable method.
    if increase_largest_group:
        if len(sorted_grouped_cards) > 0:
            sorted_grouped_cards[0] += 5 - sum(sorted_grouped_cards)
        else:
            sorted_grouped_cards.append(5)

    return sorted_grouped_cards


def has_group_with_size(groups, size):
    for group in groups:
        if groups[group] == size:
            return True
    return False


def amount_of_jokers(hand):
    return sum([1 for h in hand if h == 'J'])


def determine_hand(line, filter_jokers):
    original_hand, bid = line.split()
    hand = [h for h in original_hand if h != 'J'] if filter_jokers else original_hand
    grouped_cards = group_cards(hand, filter_jokers)

    hand_type = sum([g * -i for i, g in enumerate(grouped_cards)])
    # This is the readable method. But in fact it is only needed to calculate an order. Which can be done by a simple
    # function as done above this comment. It is important to keep the amount of cards the same however and this is
    # accomplished by adding the J cards back in the group_cards method into the largest group.
    # match len(grouped_cards):
    #     case 1:
    #         hand_type = FIVE_OF_A_KIND
    #     case 2:
    #         hand_type = FULL_HOUSE if has_group_with_size(grouped_cards, 3) else FOUR_OF_A_KIND
    #     case 3:
    #         hand_type = THREE_OF_A_KIND if has_group_with_size(grouped_cards, 3) else TWO_PAIR
    #     case 4:
    #         hand_type = ONE_PAIR
    #     case _:
    #         hand_type = HIGH_CARD

    return hand_type, [STRENGTHS[h] for h in original_hand], int(bid)


def solve(data, filter_jokers=False):
    hands = [determine_hand(line, filter_jokers) for line in data]
    sorted_hands = sorted(hands, key=lambda x: (x[0], x[1][0], x[1][1], x[1][2], x[1][3], x[1][4]))

    return sum([(i + 1) * h[2] for i, h in enumerate(sorted_hands)])

tst_input = Utils.read_input(f"input/day{day}_tst_input.txt")
puzzle_input = Utils.read_input(f"input/day{day}_input.txt")


print("Part 1")
p1_tst_result = solve(tst_input)
print(f"Test solution: {p1_tst_result}.")
if p1_tst_result == p1_expected_tst_result:
    p1_result = solve(puzzle_input)
    submit(p1_result, part="a", day=day, year=year)

print()
print("Part 2")
STRENGTHS["J"] = 1
p2_tst_result = solve(tst_input, True)
print(f"Test solution: {p2_tst_result}.")
if p2_tst_result == p2_expected_tst_result:
    p2_result = solve(puzzle_input, True)
    print(f"Puzzle solution: {p2_result}.")
    submit(p2_result, part="b", day=day, year=year)
