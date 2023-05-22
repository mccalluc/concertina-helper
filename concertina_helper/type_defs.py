from __future__ import annotations
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Iterable

from pyabc2 import Pitch as AbcPitch


@dataclass(frozen=True)
class Pitch:
    '''
    Immutable class representing a musical pitch.
    '''
    name: str

    # TODO: post_init validation: fail if name != normalized name

    @property
    def _pitch(self) -> AbcPitch:
        return AbcPitch.from_name(self.name)

    @property
    def class_name(self) -> str:
        return self._pitch.class_name

    def transpose(self, semitones: int) -> Pitch:
        return Pitch(AbcPitch(self._pitch.value + semitones).name)

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Any) -> bool:
        if type(self) != type(other):
            raise TypeError('mixed operand types')
        return self._pitch.value == other._pitch.value


@dataclass(frozen=True)
class PitchMatrix:
    '''
    Represents the pitches that can be produced by one half of a concertina,
    on either the push or pull, if bisonoric.
    '''
    matrix: tuple[tuple[Pitch, ...], ...]

    def transpose(self, semitones: int) -> PitchMatrix:
        return PitchMatrix(
            tuple(
                tuple(
                    proxy.transpose(semitones)
                    for proxy in row
                )
                for row in self.matrix
            )
        )

    def __getitem__(self, i: int) -> tuple[Pitch, ...]:
        return self.matrix[i]

    def __iter__(self) -> Iterator[tuple[Pitch, ...]]:
        return iter(self.matrix)


@dataclass(frozen=True)
class Mask:
    '''
    A boolean matix. `True` represents a key held down.

    >>> Mask(((True, False),)) | Mask(((False, True),))
    Mask(bool_matrix=((True, True),))
    '''
    bool_matrix: tuple[tuple[bool, ...], ...]

    @property
    def shape(self) -> Iterable[int]:
        return [len(row) for row in self.bool_matrix]

    def __getitem__(self, i: int) -> tuple[bool, ...]:
        return self.bool_matrix[i]

    def __iter__(self) -> Iterator[tuple[bool, ...]]:
        return iter(self.bool_matrix)

    def __or__(self, other: Any) -> Mask:
        if type(self) != type(other):
            raise TypeError('mixed operand types')
        if self.shape != other.shape:
            raise ValueError('different shapes')
        return Mask(
            tuple(
                tuple(
                    self_bool or other_bool
                    for self_bool, other_bool
                    in zip(self_row, other_row)
                )
                for self_row, other_row
                in zip(self, other)
            )
        )


Shape = tuple[Iterable[int], Iterable[int]]
'''
Describes the button arrangement of an instrument:
respectively the left and right faces, and for each face,
the number of buttons in each row.
'''

PitchToStr = Callable[[Pitch], str]
'''
A function which takes a pitch and returns a string.
(Should the octave number be printed?
Should unicode characters be used for accidentals?
Those sort of details are handled by the function.)
'''


class Direction(Enum):
    '''
    `PUSH` and `PULL`are paired with a unisonoric fingering
    to create a bisonoric fingering
    '''
    PUSH = auto()
    PULL = auto()

    def __repr__(self) -> str:
        return f'Direction.{self.name}'


@dataclass(frozen=True, kw_only=True)
class Annotation:
    pitch: Pitch
    measure: int
