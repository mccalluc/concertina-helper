import re

import pytest

from concertina_helper.layouts.unisonoric import (
    UnisonoricLayout, UnisonoricFingering)
from concertina_helper.layouts.bisonoric import (
    BisonoricLayout, BisonoricFingering,
    Direction)
from concertina_helper.layouts.layout_loader import (
    _names_to_pitches, load_bisonoric_layout_by_name)
from concertina_helper.type_defs import Mask, Pitch


u_layout = UnisonoricLayout(
    _names_to_pitches(
        [['C4', 'E4', 'G4'],
         ['G4', 'B4', 'D5']]),
    _names_to_pitches(
        [['C5', 'E5', 'G5'],
         ['G5', 'B5', 'D6']]),
)

weird_layout = UnisonoricLayout(
    _names_to_pitches(
        [['C4'],
         ['G4', 'B4']]),
    _names_to_pitches(
        [['C5', 'E5', 'G5'],
         ['G5', 'B5', 'D6', 'G6']]),
)


def test_load_bisonoric_layout_by_name_invalid():
    with pytest.raises(ValueError, match='invalid layout name'):
        load_bisonoric_layout_by_name('.')


def test_load_bisonoric_layout_by_name_missing():
    with pytest.raises(FileNotFoundError):
        load_bisonoric_layout_by_name('no_such')


class TestUnisonoricLayout:
    def test_repr(self):
        assert "UnisonoricLayout(left=PitchMatrix" in repr(u_layout)

    def test_str(self):
        assert str(u_layout) == \
            'C4  E4  G4      C5  E5  G5\n' \
            'G4  B4  D5      G5  B5  D6'

    def test_shape(self):
        assert weird_layout.shape == ([1, 2], [3, 4])

    def test_get_fingerings(self):
        fingerings = u_layout.get_fingerings(Pitch('G4'))
        assert len(fingerings) == 2
        assert any([
            fingering.left_mask == Mask(((False, False, False), (True, False, False)))
            for fingering in fingerings])
        assert any([
            fingering.left_mask == Mask(((False, False, True), (False, False, False)))
            for fingering in fingerings])
        assert all(
            fingering.right_mask == Mask(((False, False, False), (False, False, False)))
            for fingering in fingerings)
        assert all(fingering.get_pitches() == {Pitch('G4')} for fingering in fingerings)

    def test_mixed_layout_union_invalid(self):
        u_fingering = set(u_layout.get_fingerings(
            Pitch('C4'))).pop()
        weird_fingering = set(weird_layout.get_fingerings(
            Pitch('C4'))).pop()
        with pytest.raises(ValueError):
            u_fingering | weird_fingering

    def test_out_of_range(self):
        assert u_layout.get_fingerings(Pitch('C0')) == set()


b_layout = BisonoricLayout(
    push_layout=u_layout,
    pull_layout=UnisonoricLayout(
        _names_to_pitches([['D4', 'F4', 'A4'],
                           ['A4', 'C5', 'E5']]),
        _names_to_pitches([['B4', 'D5', 'F5'],
                           ['F#5', 'A5', 'C6']])
    )
)


class TestBisonoricLayout:
    def test_repr(self):
        assert "BisonoricLayout(push_layout=UnisonoricLayout(" \
            + "left=PitchMatrix" in repr(b_layout)

    def test_str(self):
        assert str(b_layout) == \
            'PUSH:\n' \
            'C4  E4  G4      C5  E5  G5\n' \
            'G4  B4  D5      G5  B5  D6\n' \
            'PULL:\n' \
            'D4  F4  A4      B4  D5  F5\n' \
            'A4  C5  E5      F#5 A5  C6'

    def test_transpose(self):
        assert str(b_layout.transpose(-2)) == \
            'PUSH:\n' \
            'Bb3 D4  F4      Bb4 D5  F5\n' \
            'F4  A4  C5      F5  A5  C6\n' \
            'PULL:\n' \
            'C4  Eb4 G4      A4  C5  Eb5\n' \
            'G4  Bb4 D5      E5  G5  Bb5'

    def test_shape(self):
        weird_bisonoric_layout = BisonoricLayout(
            push_layout=weird_layout, pull_layout=weird_layout)
        assert weird_bisonoric_layout.shape == ([1, 2], [3, 4])

    def test_shape_validation(self):
        with pytest.raises(ValueError, match=re.escape(
                'Push and pull layout shapes must match: '
                '([3, 3], [3, 3]) != ([1, 2], [3, 4])')):
            BisonoricLayout(push_layout=u_layout, pull_layout=weird_layout)

    def test_get_fingerings(self):
        fingerings = b_layout.get_fingerings(Pitch('B4'))
        assert len(fingerings) == 2
        fingering_1 = list(fingerings)[0]
        left_11 = fingering_1.left_mask[1][1]
        right_00 = fingering_1.right_mask[0][0]
        assert (
            fingering_1.direction == Direction.PUSH and left_11
            or fingering_1.direction == Direction.PULL and right_00
        )
        assert all(fingering.get_pitches() == {Pitch('B4')} for fingering in fingerings)


u_fingering = UnisonoricFingering(
    u_layout,
    Mask(((False, False, True),
          (True, False, False))),
    Mask(((False, False, True),
          (True, False, False))))


class TestUnisonoricFingering:
    def test_repr(self):
        r = repr(u_fingering)
        assert "UnisonoricFingering(layout=UnisonoricLayout(" \
            "left=PitchMatrix(matrix=" in r
        assert "bool_matrix=((False, False, True), (True, False, False))" in r

    def test_str(self):
        assert str(u_fingering) == \
            '--- --- G4     --- --- G5\n' \
            'G4  --- ---    G5  --- ---'

    def test_format_default(self):
        assert u_fingering.format() == \
            '..@   ..@\n' \
            '@..   @..'

    def test_format_custom(self):
        assert u_fingering.format(
            button_down_f=lambda pitch: pitch.class_name.ljust(2),
            button_up_f=lambda _: '. ') == \
            '. . G    . . G\n' \
            'G . .    G . .'

    def test_invalid_union(self):
        with pytest.raises(TypeError):
            u_fingering | 'not a fingering!'


b_fingering = BisonoricFingering(Direction.PUSH, u_fingering)


class TestBisonoricFingering:
    def test_repr(self):
        assert 'BisonoricFingering(direction=Direction.PUSH, ' \
            '_fingering=UnisonoricFingering(' \
            in repr(b_fingering)

    def test_str(self):
        assert str(b_fingering) == \
            'PUSH:\n' \
            '--- --- G4     --- --- G5\n' \
            'G4  --- ---    G5  --- ---'

    def test_format_default(self):
        assert b_fingering.format() == \
            'PUSH:\n' \
            '..@   ..@\n' \
            '@..   @..'

    def test_format_custom(self):
        assert b_fingering.format(
            button_down_f=lambda pitch: pitch.class_name.ljust(2),
            button_up_f=lambda _: '. ') == \
            'PUSH:\n' \
            '. . G    . . G\n' \
            'G . .    G . .'

    def test_invalid_union(self):
        with pytest.raises(TypeError):
            b_fingering | 'not a fingering!'
