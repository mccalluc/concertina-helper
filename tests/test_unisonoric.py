import pytest

from concertina_helper.layouts.unisonoric import (
    UnisonoricLayout, UnisonoricFingering)
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


def test_layout_repr():
    assert "UnisonoricLayout(left=PitchMatrix" in repr(u_layout)


def test_layout_str():
    assert str(u_layout) == \
        'C4  E4  G4      C5  E5  G5\n' \
        'G4  B4  D5      G5  B5  D6'


def test_layout_shape():
    assert weird_layout.shape == ([1, 2], [3, 4])


def test_layout_get_fingerings():
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


def test_layout_mixed_layout_union_invalid():
    u_fingering = set(u_layout.get_fingerings(
        Pitch('C4'))).pop()
    weird_fingering = set(weird_layout.get_fingerings(
        Pitch('C4'))).pop()
    with pytest.raises(ValueError):
        u_fingering | weird_fingering


def test_layout_out_of_range():
    assert u_layout.get_fingerings(Pitch('C0')) == set()


u_fingering = UnisonoricFingering(
    u_layout,
    Mask(((False, False, True),
          (True, False, False))),
    Mask(((False, False, True),
          (True, False, False))))


def test_fingering_repr():
    r = repr(u_fingering)
    assert "UnisonoricFingering(layout=UnisonoricLayout(" \
        "left=PitchMatrix(matrix=" in r
    assert "bool_matrix=((False, False, True), (True, False, False))" in r


def test_fingering_str():
    assert str(u_fingering) == \
        '--- --- G4     --- --- G5\n' \
        'G4  --- ---    G5  --- ---'


def test_fingering_format_default():
    assert u_fingering.format() == \
        '..@   ..@\n' \
        '@..   @..'


def test_fingering_format_custom():
    assert u_fingering.format(
        button_down_f=lambda pitch: pitch.class_name.ljust(2),
        button_up_f=lambda _: '. ') == \
        '. . G    . . G\n' \
        'G . .    G . .'


def test_fingering_invalid_union():
    with pytest.raises(TypeError):
        u_fingering | 'not a fingering!'
