from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass

from pyabc2 import Pitch


@dataclass(frozen=True)
class PitchProxy:
    # pyabc2 Pitch is not hashable,
    # but we want something that is less error prone than just a string.
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
    
    def __getitem__(self, i):
        return self.matrix[i]

    def __iter__(self):
        return iter(self.matrix)


Mask = tuple[tuple[bool, ...], ...]
Shape = tuple[list[int], list[int]]
PitchProxyToStr = Callable[[PitchProxy], str]
