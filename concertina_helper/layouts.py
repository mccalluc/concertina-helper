from __future__ import annotations
from enum import Enum, auto
from collections.abc import Callable
from dataclasses import dataclass

from pyabc2 import Pitch


class Direction(Enum):
    PUSH = auto()
    PULL = auto()

    def __repr__(self):
        return f'Direction.{self.name}'


@dataclass(frozen=True)
class PitchProxy:
    # pyabc2 Pitch is not hashable,
    # but we want something that is less error prone than just a string.
    name: str

    # TODO: post_init validation: fail if name != normalized name

    @property
    def pitch(self):
        return Pitch.from_name(self.name)
    @property
    def class_name(self):
        return self.pitch.class_name


Mask = tuple[tuple[bool, ...], ...]
Shape = tuple[list[int], list[int]]
PitchProxyMatrix = tuple[tuple[PitchProxy, ...], ...]
PitchProxyToStr = Callable[[PitchProxy], str]


@dataclass(frozen=True)
class UnisonoricFingering:
    layout: UnisonoricLayout
    left_mask: Mask
    right_mask: Mask

    def __str__(self) -> str:
        filler = '--- '

        def button_down_f(pitch):
            return pitch.name.ljust(len(filler))

        def button_up_f(pitch):
            return filler
        return self.format(button_down_f, button_up_f)

    def __format_button_row(
            self,
            layout_row: tuple[PitchProxy, ...], mask_row: tuple[bool, ...],
            button_down_f: PitchProxyToStr, button_up_f: PitchProxyToStr) -> str:
        return ''.join(
            (button_down_f if button else button_up_f)(pitch)
            for pitch, button in zip(layout_row, mask_row)
        )

    def format(
            self,
            button_down_f: PitchProxyToStr = lambda pitch: '@',
            button_up_f: PitchProxyToStr = lambda pitch: '.') -> str:
        lines = []
        enumerated_mask_rows = enumerate(zip(self.left_mask, self.right_mask))
        for i, (left_mask_row, right_mask_row) in enumerated_mask_rows:
            cols = []
            cols.append(self.__format_button_row(
                self.layout.left[i], left_mask_row,
                button_down_f, button_up_f))
            cols.append('   ')
            cols.append(self.__format_button_row(
                self.layout.right[i], right_mask_row,
                button_down_f, button_up_f))
            lines.append(''.join(cols))
        return '\n'.join(lines)


@dataclass(frozen=True)
class BisonoricFingering:
    direction: Direction
    fingering: UnisonoricFingering

    def __str__(self) -> str:
        return f'{self.direction.name}:\n{self.fingering}'

    def format(
        self,
        button_down_f: PitchProxyToStr = lambda pitch: '@',
        button_up_f: PitchProxyToStr = lambda pitch: '.',
        direction_f: Callable[[Direction], str] =
            lambda direction: direction.name) -> str:
        return f'{direction_f(self.direction)}:\n' \
            f'{self.fingering.format(button_down_f, button_up_f)}'


@dataclass(frozen=True)
class UnisonoricLayout:
    left: PitchProxyMatrix
    right: PitchProxyMatrix

    @property
    def shape(self) -> Shape:
        return (
            [len(row) for row in self.left],
            [len(row) for row in self.right],
        )

    def __list_mask_to_mask(self, list_mask: list[list[bool]]) -> Mask:
        return tuple(
            tuple(
                button for button in row
            ) for row in list_mask
        )

    def _get_masks(self):
        return (
            [[False] * len(row) for row in self.left],
            [[False] * len(row) for row in self.right]
        )

    def get_fingerings(self, pitch: Pitch) -> frozenset[UnisonoricFingering]:
        fingerings = set()
        # TODO: Clean up!
        # left:
        for i, row in enumerate(self.left):
            for j, button in enumerate(row):
                if pitch == button.pitch:
                    left, right = self._get_masks()
                    left[i][j] = True
                    fingerings.add(UnisonoricFingering(
                        self, self.__list_mask_to_mask(left),
                        self.__list_mask_to_mask(right)))
        # right:
        for i, row in enumerate(self.right):
            for j, button in enumerate(row):
                if pitch == button.pitch:
                    left, right = self._get_masks()
                    right[i][j] = True
                    fingerings.add(UnisonoricFingering(
                        self, self.__list_mask_to_mask(left),
                        self.__list_mask_to_mask(right)))
        return frozenset(fingerings)

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


@dataclass(frozen=True, kw_only=True)
class BisonoricLayout:
    push_layout: UnisonoricLayout
    pull_layout: UnisonoricLayout

    def __post_init__(self):
        if self.push_layout.shape != self.pull_layout.shape:
            raise ValueError(
                'Push and pull layout shapes must match: '
                f'{self.push_layout.shape} != {self.pull_layout.shape}')

    @property
    def shape(self) -> Shape:
        return (
            [len(row) for row in self.push_layout.left],
            [len(row) for row in self.push_layout.right],
        )

    def get_fingerings(self, pitch: Pitch) -> set[BisonoricFingering]:
        push_fingerings = self.push_layout.get_fingerings(pitch)
        pull_fingerings = self.pull_layout.get_fingerings(pitch)
        return (
            {BisonoricFingering(Direction.PUSH, pf) for pf in push_fingerings} |
            {BisonoricFingering(Direction.PULL, pf) for pf in pull_fingerings}
        )

    def __str__(self) -> str:
        return f'{Direction.PUSH.name}:\n{self.push_layout}\n' \
            f'{Direction.PULL.name}:\n{self.pull_layout}'


def _names_to_pitches(matrix: list[list[str]]) -> PitchProxyMatrix:
    '''
    >>> pitch_matrix = _names_to_pitches([['C4']])
    >>> pitch_matrix[0][0].name
    'C4'
    '''
    return tuple(tuple(PitchProxy(name) for name in row) for row in matrix)


cg_anglo_wheatstone_layout = BisonoricLayout(
    push_layout=UnisonoricLayout(
        _names_to_pitches(
            [['E3', 'A3', 'C#4', 'A4', 'G#4'],
             ['C3', 'G3', 'C4', 'E4', 'G4'],
                ['B3', 'D4', 'G4', 'B4', 'D5']]),
        _names_to_pitches(
            [['C#5', 'A5', 'G#5', 'C#6', 'A6'],
             ['C5', 'E5', 'G5', 'C6', 'E6'],
                ['G5', 'B5', 'D6', 'G6', 'B6']]),
    ),
    pull_layout=UnisonoricLayout(
        _names_to_pitches(
            [['F3', 'Bb3', 'D#4', 'G4', 'Bb4'],
             ['G3', 'B3', 'D4', 'F4', 'A4'],
                ['A3', 'F#4', 'A4', 'C5', 'E5']]),
        _names_to_pitches(
            [['D#5', 'G5', 'Bb5', 'D#6', 'F6'],
             ['B4', 'D5', 'F5', 'A5', 'B5'],
                ['F#5', 'A5', 'C6', 'E6', 'F#6']])
    ),
)
