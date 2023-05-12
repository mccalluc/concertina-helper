from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TypeVar, Generic

from ..type_defs import Shape, Pitch, PitchToStr


T = TypeVar('T')


class Fingering(ABC):
    @abstractmethod
    def format(self, button_down_f: PitchToStr,
               button_up_f: PitchToStr,
               direction_f: Callable) -> str:
        '''
        Returns a formatted, human-readable string
        '''

    @abstractmethod
    def get_pitches(self) -> set[Pitch]:
        '''
        Returns the pitches that would be produced by this fingering
        '''


class Layout(ABC, Generic[T]):
    @property
    @abstractmethod
    def shape(self) -> Shape:
        '''
        Returns tuple representing the number of buttons in each row, left and right.
        '''

    @abstractmethod
    def get_fingerings(self, pitch: Pitch) -> set[T]:
        '''
        Returns a set of possible fingerings on the layout for a given pitch
        '''

    @abstractmethod
    def transpose(self, semitones: int) -> Layout:
        '''
        Given a number of semitones, return a new layout,
        transposed up or down.
        '''
