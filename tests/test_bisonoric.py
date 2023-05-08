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


b_layout = BisonoricLayout(
    push_layout=u_layout,
    pull_layout=UnisonoricLayout(
        _names_to_pitches([['D4', 'F4', 'A4'],
                           ['A4', 'C5', 'E5']]),
        _names_to_pitches([['B4', 'D5', 'F5'],
                           ['F#5', 'A5', 'C6']])
    )
)


def test_layout_repr():
    assert "BisonoricLayout(push_layout=UnisonoricLayout(" \
        + "left=PitchMatrix" in repr(b_layout)


def test_layout_str():
    assert str(b_layout) == \
        'PUSH:\n' \
        'C4  E4  G4      C5  E5  G5\n' \
        'G4  B4  D5      G5  B5  D6\n' \
        'PULL:\n' \
        'D4  F4  A4      B4  D5  F5\n' \
        'A4  C5  E5      F#5 A5  C6'


def test_layout_transpose():
    assert str(b_layout.transpose(-2)) == \
        'PUSH:\n' \
        'Bb3 D4  F4      Bb4 D5  F5\n' \
        'F4  A4  C5      F5  A5  C6\n' \
        'PULL:\n' \
        'C4  Eb4 G4      A4  C5  Eb5\n' \
        'G4  Bb4 D5      E5  G5  Bb5'


def test_layout_shape():
    weird_bisonoric_layout = BisonoricLayout(
        push_layout=weird_layout, pull_layout=weird_layout)
    assert weird_bisonoric_layout.shape == ([1, 2], [3, 4])


def test_layout_shape_validation():
    with pytest.raises(ValueError, match=re.escape(
            'Push and pull layout shapes must match: '
            '([3, 3], [3, 3]) != ([1, 2], [3, 4])')):
        BisonoricLayout(push_layout=u_layout, pull_layout=weird_layout)


def test_layout_get_fingerings():
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


b_fingering = BisonoricFingering(Direction.PUSH, u_fingering)


def test_fingering_repr():
    assert 'BisonoricFingering(direction=Direction.PUSH, ' \
        '_fingering=UnisonoricFingering(' \
        in repr(b_fingering)


def test_fingering_str():
    assert str(b_fingering) == \
        'PUSH:\n' \
        '--- --- G4     --- --- G5\n' \
        'G4  --- ---    G5  --- ---'


def test_fingering_format_default():
    assert b_fingering.format() == \
        'PUSH:\n' \
        '..@   ..@\n' \
        '@..   @..'


def test_fingering_format_custom():
    assert b_fingering.format(
        button_down_f=lambda pitch: pitch.class_name.ljust(2),
        button_up_f=lambda _: '. ') == \
        'PUSH:\n' \
        '. . G    . . G\n' \
        'G . .    G . .'


def test_fingering_invalid_union():
    with pytest.raises(TypeError):
        b_fingering | 'not a fingering!'
