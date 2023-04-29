import re

import pytest

from pyabc2 import Pitch

from concertina_helper.layouts.unisonoric import (
    UnisonoricLayout, UnisonoricFingering)
from concertina_helper.layouts.bisonoric import (
    BisonoricLayout, BisonoricFingering,
    Direction)
from concertina_helper.layouts.layout_loader import (
    _names_to_pitches, load_bisonoric_layout_by_name)


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
        assert "UnisonoricLayout(left=((PitchProxy(name='C4')," in repr(u_layout)

    def test_str(self):
        assert str(u_layout) == \
            'C4  E4  G4      C5  E5  G5 \n' \
            'G4  B4  D5      G5  B5  D6 '

    def test_shape(self):
        assert weird_layout.shape == ([1, 2], [3, 4])

    def test_get_fingerings(self):
        fingerings = u_layout.get_fingerings(Pitch.from_name('G4'))
        assert len(fingerings) == 2
        fingering_1 = list(fingerings)[0]
        # TODO: get rid of "or"
        assert (
            fingering_1.left_mask == ((False, False, False), (True, False, False))
            or fingering_1.left_mask == ((False, False, True), (False, False, False))
        )
        assert fingering_1.right_mask == (
            (False, False, False), (False, False, False))


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
        assert "BisonoricLayout(push_layout=UnisonoricLayout(left=((" in repr(b_layout)

    def test_str(self):
        assert str(b_layout) == \
            'PUSH:\n' \
            'C4  E4  G4      C5  E5  G5 \n' \
            'G4  B4  D5      G5  B5  D6 \n' \
            'PULL:\n' \
            'D4  F4  A4      B4  D5  F5 \n' \
            'A4  C5  E5      F#5 A5  C6 '

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
        fingerings = b_layout.get_fingerings(Pitch.from_name('B4'))
        assert len(fingerings) == 2
        fingering_1 = list(fingerings)[0]
        assert (
            fingering_1.direction == Direction.PUSH
            and fingering_1.fingering.left_mask[1][1]
            or fingering_1.direction == Direction.PULL
            and fingering_1.fingering.right_mask[0][0]
        )


u_fingering = UnisonoricFingering(
    u_layout,
    [[False, False, True],
     [True, False, False]],
    [[False, False, True],
     [True, False, False]])


class TestUnisonoricFingering:
    def test_repr(self):
        r = repr(u_fingering)
        assert "UnisonoricFingering(layout=UnisonoricLayout(" \
            "left=((PitchProxy(name='C4')" in r
        assert "left_mask=[[False, False, True], [True, False, False]]" in r

    def test_str(self):
        assert str(u_fingering) == \
            '--- --- G4     --- --- G5  \n' \
            'G4  --- ---    G5  --- --- '

    def test_format_default(self):
        assert u_fingering.format() == \
            '..@   ..@\n' \
            '@..   @..'

    def test_format_custom(self):
        assert u_fingering.format(
            button_down_f=lambda pitch: pitch.class_name.ljust(2),
            button_up_f=lambda _: '. ') == \
            '. . G    . . G \n' \
            'G . .    G . . '


b_fingering = BisonoricFingering(Direction.PUSH, u_fingering)


class TestBisonoricFingering:
    def test_repr(self):
        assert 'BisonoricFingering(direction=Direction.PUSH, ' \
            'fingering=UnisonoricFingering(' \
            in repr(b_fingering)

    def test_str(self):
        assert str(b_fingering) == \
            'PUSH:\n' \
            '--- --- G4     --- --- G5  \n' \
            'G4  --- ---    G5  --- --- '

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
            '. . G    . . G \n' \
            'G . .    G . . '
