from __future__ import annotations
from enum import Enum, auto
from pyabc2 import Pitch


class Direction(Enum):
    PUSH = auto()
    PULL = auto()


Mask = list[list[bool]]


class UnisonoricFingering:
    def __init__(self, layout: UnisonoricLayout, left_mask: Mask, right_mask: Mask):
        self.layout = layout
        self.left_mask = left_mask
        self.right_mask = right_mask

    def __repr__(self) -> str:
        return f'UnisonoricFingering({repr(self.layout)}, ' \
            f'{repr(self.left_mask)}, {repr(self.right_mask)})'

    def __str__(self) -> str:
        lines = []
        enumerated_mask_rows = enumerate(zip(self.left_mask, self.right_mask))
        for i, (left_mask_row, right_mask_row) in enumerated_mask_rows:
            cols = []
            filler = '---'
            for j, button in enumerate(left_mask_row):
                cols.append(self.layout.left[i][j].name.ljust(
                    len(filler)) if button else filler)
            cols.append('   ')
            for j, button in enumerate(right_mask_row):
                cols.append(self.layout.right[i][j].name.ljust(
                    len(filler)) if button else filler)
            lines.append(' '.join(cols))
        return '\n'.join(lines)


class BisonoricFingering:
    def __init__(self, direction: Direction, fingering: UnisonoricFingering):
        self.direction = direction
        self.fingering = fingering

    def __repr__(self) -> str:
        return f'BisonoricFingering(Direction.{self.direction.name}, ' \
            f'{repr(self.fingering)})'

    def __str__(self) -> str:
        return f'{self.direction.name}:\n{self.fingering}'


class Layout:
    pass


def split_masks(left_mask: Mask, right_mask: Mask) -> set[tuple[Mask, Mask]]:
    return set()  # TODO


class UnisonoricLayout(Layout):
    def __init__(self, left: list[list[Pitch]], right: list[list[Pitch]]):
        self.left = left
        self.right = right

    def _get_masks(self) -> tuple[Mask, Mask]:
        return (
            [[False for _ in row] for row in self.left],
            [[False for _ in row] for row in self.right]
        )

    def get_fingerings(self, pitch: Pitch) -> set[UnisonoricFingering]:
        fingerings = set()
        # left:
        for i, row in enumerate(self.left):
            for j, button in enumerate(row):
                if pitch == button:
                    left, right = self._get_masks()
                    left[i][j] = True
                    fingerings.add(UnisonoricFingering(self, left, right))
        # right:
        for i, row in enumerate(self.right):
            for j, button in enumerate(row):
                if pitch == button:
                    left, right = self._get_masks()
                    right[i][j] = True
                    fingerings.add(UnisonoricFingering(self, left, right))
        return fingerings

    def __repr__(self) -> str:
        return f'UnisonoricLayout({repr(self.left)}, {repr(self.right)})'

    def __str__(self) -> str:
        lines = []
        for left_row, right_row in zip(self.left, self.right):
            cols = []
            for button in left_row:
                cols.append(button.name.ljust(3))
            cols.append('   ')
            for button in right_row:
                cols.append(button.name.ljust(3))
            lines.append(' '.join(cols))
        return '\n'.join(lines)


class BisonoricLayout(Layout):
    def __init__(self, push_layout: UnisonoricLayout, pull_layout: UnisonoricLayout):
        self.push_layout = push_layout
        self.pull_layout = pull_layout

    def get_fingerings(self, pitch: Pitch) -> set[BisonoricFingering]:
        push_fingerings = self.push_layout.get_fingerings(pitch)
        pull_fingerings = self.pull_layout.get_fingerings(pitch)
        return (
            {BisonoricFingering(Direction.PUSH, pf) for pf in push_fingerings} |
            {BisonoricFingering(Direction.PULL, pf) for pf in pull_fingerings}
        )

    def __repr__(self) -> str:
        return f'BisonoricLayout({repr(self.push_layout)}, {repr(self.pull_layout)})'

    def __str__(self) -> str:
        return f'{Direction.PUSH.name}:\n{self.push_layout}\n' \
            f'{Direction.PULL.name}:\n{self.pull_layout}'


def _names_to_pitches(matrix: list[list[str]]) -> list[list[Pitch]]:
    '''
    >>> pitch_matrix = _names_to_pitches([['C4']])
    >>> pitch_matrix[0][0].name
    'C4'
    '''
    return [[Pitch.from_name(name) for name in row] for row in matrix]


__cg_anglo_wheatstone_push_layout = UnisonoricLayout(
    _names_to_pitches(
        [['E3', 'A3', 'C#4', 'A4', 'G#4'],
         ['C3', 'G3', 'C4', 'E4', 'G4'],
            ['B3', 'D4', 'G4', 'B4', 'D5']]),
    _names_to_pitches(
        [['C#5', 'A5', 'G#5', 'C#6', 'A6'],
         ['C5', 'E5', 'G5', 'C6', 'E6'],
            ['G5', 'B5', 'D6', 'G6', 'B6']]),
)

__cg_anglo_wheatstone_pull_layout = UnisonoricLayout(
    _names_to_pitches(
        [['F3', 'Bb3', 'D#4', 'G4', 'Bb4'],
         ['G3', 'B3', 'D4', 'F4', 'A4'],
            ['A3', 'F#4', 'A4', 'C5', 'E5']]),
    _names_to_pitches(
        [['D#5', 'G5', 'Bb5', 'D#6', 'F6'],
         ['B4', 'D5', 'F5', 'A5', 'B5'],
            ['F#5', 'A5', 'C6', 'E6', 'F#6']])
)

cg_anglo_wheatstone_layout = BisonoricLayout(
    push_layout=__cg_anglo_wheatstone_push_layout,
    pull_layout=__cg_anglo_wheatstone_pull_layout,
)
