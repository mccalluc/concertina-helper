from __future__ import annotations
from typing import Any
from collections.abc import Callable
from dataclasses import dataclass

from .unisonoric import UnisonoricFingering, UnisonoricLayout
from ..type_defs import Shape, PitchToStr, Mask, Pitch, Direction, Annotation
from .base_classes import Layout, Fingering


@dataclass(frozen=True, kw_only=True)
class BisonoricLayout(Layout['BisonoricFingering']):
    '''
    Represents a bisonoric concertina layout:
    the layout of the buttons on the left and right,
    and the pitches they produce on push and pull.

    >>> from concertina_helper.layouts.layout_loader import (
    ...     load_bisonoric_layout_by_name)
    >>> layout = load_bisonoric_layout_by_name('30_wheatstone_cg')
    >>> print(layout)
    PUSH:
    E3  A3  C#4 A4  G#4     C#5 A5  G#5 C#6 A6
    C3  G3  C4  E4  G4      C5  E5  G5  C6  E6
    B3  D4  G4  B4  D5      G5  B5  D6  G6  B6
    PULL:
    F3  Bb3 D#4 G4  Bb4     D#5 G5  Bb5 D#6 F6
    G3  B3  D4  F4  A4      B4  D5  F5  A5  B5
    A3  F#4 A4  C5  E5      F#5 A5  C6  E6  F#6

    With a layout, you can get all fingerings for a particular pitch.
    Fingerings can be combined to produce chords:

    >>> c = layout.get_fingerings(Pitch('C4')).pop()
    >>> e = layout.get_fingerings(Pitch('E4')).pop()
    >>> print(c | e)
    PUSH:
    --- --- --- --- ---    --- --- --- --- ---
    --- --- C4  E4  ---    --- --- --- --- ---
    --- --- --- --- ---    --- --- --- --- ---

    Fingerings with different bellow directions can not be combined:
    >>> f = layout.get_fingerings(Pitch('F4')).pop()
    >>> print(c | f)
    Traceback (most recent call last):
    ...
    ValueError: different bellows directions
    '''
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
        '''
        Given a pitch, return all possible fingerings as a set.
        '''
        push_fingerings = self.push_layout.get_fingerings(pitch)
        pull_fingerings = self.pull_layout.get_fingerings(pitch)
        return (
            {BisonoricFingering(Direction.PUSH, pf) for pf in push_fingerings} |
            {BisonoricFingering(Direction.PULL, pf) for pf in pull_fingerings}
        )

    def __str__(self) -> str:
        return f'{Direction.PUSH.name}:\n{self.push_layout}\n' \
            f'{Direction.PULL.name}:\n{self.pull_layout}'

    def transpose(self, semitones: int) -> BisonoricLayout:
        '''
        Given a number of semitones, return a new layout,
        transposed up or down.
        '''
        return BisonoricLayout(
            push_layout=self.push_layout.transpose(semitones),
            pull_layout=self.pull_layout.transpose(semitones))


@dataclass(frozen=True)
class BisonoricFingering(Fingering):
    '''
    Represents a fingering on a bisonoric concertina.
    '''
    direction: Direction
    _fingering: UnisonoricFingering

    @property
    def left_mask(self) -> Mask:
        return self._fingering.left_mask

    @property
    def right_mask(self) -> Mask:
        return self._fingering.right_mask

    def __str__(self) -> str:
        return f'{self.direction.name}:\n{self._fingering}'

    def format(
        self,
        button_down_f: PitchToStr = lambda pitch: '@',
        button_up_f: PitchToStr = lambda pitch: '.',
        direction_f: Callable[[Direction], str] =
            lambda direction: direction.name) -> str:
        return f'{direction_f(self.direction)}:\n' \
            f'{self._fingering.format(button_down_f, button_up_f)}'

    def __or__(self, other: Any) -> BisonoricFingering:
        if type(self) != type(other):
            raise TypeError('mixed operand types')
        if self.direction != other.direction:
            raise ValueError('different bellows directions')
        return BisonoricFingering(self.direction, self._fingering | other._fingering)

    def get_pitches(self) -> set[Pitch]:
        return self._fingering.get_pitches()


@dataclass(frozen=True, kw_only=True)
class AnnotatedBisonoricFingering:
    '''
    Adds contextual information to the fingering
    that is useful in finding the best fingering for a tune.
    '''
    fingering: BisonoricFingering
    annotation: Annotation

    def __str__(self) -> str:
        a = self.annotation
        return f'Measure {a.measure} - {a.pitch}\n{self.fingering}'

    def format(  # pragma: no branch
            self,
            button_down_f: PitchToStr = lambda pitch: '@',
            button_up_f: PitchToStr = lambda pitch: '.',
            direction_f: Callable[[Direction], str] =
            lambda direction: direction.name) -> str:
        a = self.annotation
        formatted = self.fingering.format(
            button_down_f=button_down_f,
            button_up_f=button_up_f,
            direction_f=direction_f)
        return f'Measure {a.measure} - {a.pitch}\n{formatted}'
