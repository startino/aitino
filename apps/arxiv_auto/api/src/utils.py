from typing import List


def majority_vote(bool_list: List[bool]) -> bool:
    return sum(bool_list) > len(bool_list) / 2


def calculate_certainty_from_bools(bool_list: List[bool]) -> float:
    length = len(bool_list)
    total = sum(bool_list)

    true_certainty = total / length
    false_certainty = (length - total) / length

    return max(true_certainty, false_certainty)

