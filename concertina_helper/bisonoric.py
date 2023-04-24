from __future__ import annotations
from enum import Enum, auto
from collections.abc import Callable
from dataclasses import dataclass

from pyabc2 import Pitch

from .unisonoric import UnisonoricFingering, UnisonoricLayout
from .util import *


class Direction(Enum):
    PUSH = auto()
    PULL = auto()

    def __repr__(self):
        return f'Direction.{self.name}'


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


@dataclass(frozen=True, kw_only=True)
class AnnotatedBisonoricFingering:
    fingering: BisonoricFingering
    measure: int


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
