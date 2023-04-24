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
    def pitch(self):
        return Pitch.from_name(self.name)

    @property
    def class_name(self):
        return self.pitch.class_name


Mask = tuple[tuple[bool, ...], ...]
Shape = tuple[list[int], list[int]]
PitchProxyMatrix = tuple[tuple[PitchProxy, ...], ...]
PitchProxyToStr = Callable[[PitchProxy], str]
