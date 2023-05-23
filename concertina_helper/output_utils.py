from __future__ import annotations
from collections.abc import Iterable

from .layouts.bisonoric import AnnotatedBisonoricFingering
from .type_defs import Direction


def condense(fingerings: Iterable[AnnotatedBisonoricFingering]) -> str:
    '''
    Given a sequence of fingerings,
    returns a compact, tab delimitted string representation
    of the entire sequence, up to 20 fingerings.

    Buttons to hit while pushing are represented like this:
    > ➀➁➂

    while buttons for the pull are represented:
    > ➊➋➌
    '''
    chars = {
        Direction.PUSH: '➀➁➂➃➄➅➆➇➈➉⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳',
        Direction.PULL: '➊➋➌➍➎➏➐➑➒➓⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴'
    }

    f_list = list(fingerings)
    max_len = len(chars[Direction.PUSH])
    if len(f_list) > max_len:
        raise ValueError(
            f'Length of fingerings ({len(f_list)}) '
            f'greater than allowed ({max_len})')

    left = [[''] * row_len for row_len in f_list[0].fingering.left_mask.shape]
    right = [[''] * row_len for row_len in f_list[0].fingering.right_mask.shape]

    for index, f in enumerate(f_list):
        for i, row in enumerate(f.fingering.left_mask):
            for j, button in enumerate(row):
                if button:
                    left[i][j] += chars[f.fingering.direction][index]
        for i, row in enumerate(f.fingering.right_mask):
            for j, button in enumerate(row):
                if button:
                    right[i][j] += chars[f.fingering.direction][index]

    lines = []
    for left_row, right_row in zip(left, right):
        line = []
        for finger_string in left_row:
            line.append(finger_string or '.')
        line.append(' ')
        for finger_string in right_row:
            line.append(finger_string or '.')
        lines.append(' '.join(line))
    return '\n'.join(lines)
