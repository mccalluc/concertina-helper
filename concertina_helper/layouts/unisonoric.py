from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from collections.abc import Callable

from ..type_defs import Shape, Pitch, PitchToStr, PitchMatrix, Mask, Direction
from .base_classes import Layout, Fingering


@dataclass(frozen=True)
class UnisonoricLayout(Layout['UnisonoricFingering']):
    left: PitchMatrix
    right: PitchMatrix

    @property
    def shape(self) -> Shape:
        return (
            [len(row) for row in self.left],
            [len(row) for row in self.right],
        )

    def __make_masks(self, pitch: Pitch, pm: PitchMatrix) -> set[Mask]:
        masks = set()
        for i, row in enumerate(pm):
            for j, button in enumerate(row):
                if pitch == button:
                    mutable_mask = [[False] * len(row) for row in pm]
                    mutable_mask[i][j] = True
                    mask = Mask(tuple(
                        tuple(row) for row in mutable_mask
                    ))
                    masks.add(mask)
        return masks

    def get_fingerings(self, pitch: Pitch) -> set[UnisonoricFingering]:
        fingerings = set()

        left_all_false = Mask(tuple((False,) * len(row) for row in self.left))
        right_all_false = Mask(tuple((False,) * len(row) for row in self.right))

        for left_mask in self.__make_masks(pitch, self.left):
            fingerings.add(UnisonoricFingering(self, left_mask, right_all_false))
        for right_mask in self.__make_masks(pitch, self.right):
            fingerings.add(UnisonoricFingering(self, left_all_false, right_mask))
        return fingerings

    def __str__(self) -> str:
        lines = []
        for left_row, right_row in zip(self.left, self.right):
            cols = []
            for button in left_row:
                cols.append(str(button).ljust(3))
            cols.append('   ')
            for button in right_row:
                cols.append(str(button).ljust(3))
            lines.append(' '.join(cols).strip())
        return '\n'.join(lines)

    def transpose(self, semitones: int) -> UnisonoricLayout:
        return UnisonoricLayout(
            self.left.transpose(semitones),
            self.right.transpose(semitones))


@dataclass(frozen=True)
class UnisonoricFingering(Fingering):
    layout: UnisonoricLayout
    left_mask: Mask
    right_mask: Mask

    def __str__(self) -> str:
        filler = '--- '

        def button_down_f(pitch: Pitch) -> str:
            return str(pitch).ljust(len(filler))

        def button_up_f(pitch: Pitch) -> str:
            return filler
        return self.format(button_down_f, button_up_f)

    def __format_button_row(
            self,
            layout_row: tuple[Pitch, ...], mask_row: tuple[bool, ...],
            button_down_f: PitchToStr, button_up_f: PitchToStr) -> str:
        return ''.join(
            (button_down_f if button else button_up_f)(pitch)
            for pitch, button in zip(layout_row, mask_row)
        )

    def format(
            self,
            button_down_f: PitchToStr = lambda pitch: '@',
            button_up_f: PitchToStr = lambda pitch: '.',
            direction_f: Callable[[Direction], str] =
            lambda direction: direction.name) -> str:
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
            lines.append(''.join(cols).strip())
        return '\n'.join(lines)

    def __or__(self, other: Any) -> UnisonoricFingering:
        if type(self) != type(other):
            raise TypeError('mixed operand types')
        if self.layout != other.layout:
            raise ValueError('different layouts')
        return UnisonoricFingering(
            self.layout,
            self.left_mask | other.left_mask,
            self.right_mask | other.right_mask
        )

    def get_pitches(self) -> set[Pitch]:
        pitches = set()
        sides = [
            (self.layout.left, self.left_mask),
            (self.layout.right, self.right_mask),
        ]
        for side in sides:
            for layout_row, mask_row in zip(*side):
                for pitch, button in zip(layout_row, mask_row):
                    if button:
                        pitches.add(pitch)
        return pitches
