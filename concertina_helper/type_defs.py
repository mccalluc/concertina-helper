from __future__ import annotations
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Any

from pyabc2 import Pitch


@dataclass(frozen=True)
class PitchProxy:
    '''
    Immutable class representing a musical pitch. Wraps pyabc2's `Pitch` class.
    '''
    name: str

    # TODO: post_init validation: fail if name != normalized name

    @property
    def pitch(self) -> Pitch:
        return Pitch.from_name(self.name)

    @property
    def class_name(self) -> str:
        return self.pitch.class_name

    def transpose(self, semitones: int) -> PitchProxy:
        return PitchProxy(Pitch(self.pitch.value + semitones).name)


@dataclass(frozen=True)
class PitchProxyMatrix:
    '''
    Represents the pitches that can be produced by one half of a concertina,
    on either the push or pull, if bisonoric.
    '''
    matrix: tuple[tuple[PitchProxy, ...], ...]

    def transpose(self, semitones: int) -> PitchProxyMatrix:
        return PitchProxyMatrix(
            tuple(
                tuple(
                    proxy.transpose(semitones)
                    for proxy in row
                )
                for row in self.matrix
            )
        )

    def __getitem__(self, i: int) -> tuple[PitchProxy, ...]:
        return self.matrix[i]

    def __iter__(self) -> Iterator[tuple[PitchProxy, ...]]:
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
    def shape(self) -> list[int]:
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



Shape = tuple[list[int], list[int]]
'''
Describes the button arrangement of an instrument:
respectively the left and right faces, and for each face,
the number of buttons in each row.
'''

PitchProxyToStr = Callable[[PitchProxy], str]
'''
A function which takes a pitch and returns a string.
(Should the octave number be printed?
Should unicode characters be used for accidentals?
Those sort of details are handled by the function.)
'''
