from __future__ import annotations
from dataclasses import dataclass

from pyabc2 import Pitch

from .util import *


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
                        self,
                        self.__list_mask_to_mask(left),
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
