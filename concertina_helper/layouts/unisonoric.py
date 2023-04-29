from __future__ import annotations
from dataclasses import dataclass

from pyabc2 import Pitch

from ..type_defs import Shape, PitchProxy, PitchProxyToStr, PitchProxyMatrix, Mask


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

    def __make_masks(self, pitch: Pitch, ppm: PitchProxyMatrix) -> set[Mask]:
        masks = set()
        for i, row in enumerate(ppm):
            for j, button in enumerate(row):
                if pitch == button.pitch:
                    mutable_mask = [[False] * len(row) for row in ppm]
                    mutable_mask[i][j] = True
                    mask = tuple(
                        tuple(row) for row in mutable_mask
                    )
                    masks.add(mask)
        return masks

    def get_fingerings(self, pitch: Pitch) -> frozenset[UnisonoricFingering]:
        fingerings = set()

        left_all_false = tuple((False,) * len(row) for row in self.left)
        right_all_false = tuple((False,) * len(row) for row in self.right)

        for left_mask in self.__make_masks(pitch, self.left):
            fingerings.add(UnisonoricFingering(self, left_mask, right_all_false))
        for right_mask in self.__make_masks(pitch, self.right):
            fingerings.add(UnisonoricFingering(self, left_all_false, right_mask))
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

    def transpose(self, semitones: int) -> UnisonoricLayout:
        return UnisonoricLayout(
            self.left.transpose(semitones),
            self.right.transpose(semitones))


@dataclass(frozen=True)
class UnisonoricFingering:
    layout: UnisonoricLayout
    left_mask: Mask
    right_mask: Mask

    def __str__(self) -> str:
        filler = '--- '

        def button_down_f(pitch: PitchProxy) -> str:
            return pitch.name.ljust(len(filler))

        def button_up_f(pitch: PitchProxy) -> str:
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
