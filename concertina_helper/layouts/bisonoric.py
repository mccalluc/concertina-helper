from __future__ import annotations
from enum import Enum, auto
from collections.abc import Callable
from dataclasses import dataclass

from pyabc2 import Pitch

from .unisonoric import UnisonoricFingering, UnisonoricLayout
from ..type_defs import Shape, PitchProxyToStr


class Direction(Enum):
    PUSH = auto()
    PULL = auto()

    def __repr__(self) -> str:
        return f'Direction.{self.name}'


@dataclass(frozen=True, kw_only=True)
class BisonoricLayout:
    push_layout: UnisonoricLayout
    pull_layout: UnisonoricLayout

    def __post_init__(self) -> None:
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
