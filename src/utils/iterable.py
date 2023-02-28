from typing import Sequence, TypeVar


_T = TypeVar('_T')


def remove_duplicates_sorted_seq(seq: Sequence[_T]) -> list[_T]:
    if not seq:
        return []

    result = [seq[0]]
    for x in seq[1:]:
        if x != result[-1]:
            result.append(x)
    return result

