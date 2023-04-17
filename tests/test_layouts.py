from pyabc2 import Pitch

from layouts import (
    UnisonoricLayout, UnisonoricFingering,
    BisonoricLayout, BisonoricFingering,
    Direction, _names_to_pitches)


# Test UnisonoricLayout methods:


u_layout = UnisonoricLayout(
    _names_to_pitches(
        [['C4', 'E4', 'G4'],
         ['G4', 'B4', 'D5']]),
    _names_to_pitches(
        [['C5', 'E5', 'G5'],
         ['G5', 'B5', 'D6']]),
)


def test_UnisonoricLayout_repr():
    assert "UnisonoricLayout([[Pitch(value=48, name='C4')," in repr(u_layout)


def test_UnisonoricLayout_str():
    assert str(u_layout) == \
        'C4  E4  G4      C5  E5  G5 \n' \
        'G4  B4  D5      G5  B5  D6 '


def test_UnisonoricLayout_get_fingerings():
    fingerings = u_layout.get_fingerings(Pitch.from_name('G4'))
    assert len(fingerings) == 2
    fingering_1 = list(fingerings)[0]
    assert (
        fingering_1.left_mask == [[False, False, False], [True, False, False]]
        or fingering_1.left_mask == [[False, False, True], [False, False, False]]
    )
    assert fingering_1.right_mask == [
        [False, False, False], [False, False, False]]


# Test BisonoricLayout methods:


b_layout = BisonoricLayout(
    u_layout,
    UnisonoricLayout(
        _names_to_pitches([['D4', 'F4', 'A4'],
                           ['A4', 'C5', 'E5']]),
        _names_to_pitches([['B4', 'D5', 'F5'],
                           ['F#5', 'A5', 'C6']])
    )
)


def test_BisonoricLayout_repr():
    assert "BisonoricLayout(UnisonoricLayout([[Pitch(" in repr(b_layout)


def test_BisonoricLayout_str():
    assert str(b_layout) == \
        'PUSH:\n' \
        'C4  E4  G4      C5  E5  G5 \n' \
        'G4  B4  D5      G5  B5  D6 \n' \
        'PULL:\n' \
        'D4  F4  A4      B4  D5  F5 \n' \
        'A4  C5  E5      F#5 A5  C6 '


def test_BisonoricLayout_get_fingerings():
    fingerings = b_layout.get_fingerings(Pitch.from_name('B4'))
    assert len(fingerings) == 2
    fingering_1 = list(fingerings)[0]
    assert (
        fingering_1.direction == Direction.PUSH
        and fingering_1.fingering.left_mask[1][1]
        or fingering_1.direction == Direction.PULL
        and fingering_1.fingering.right_mask[0][0]
    )


# Test UnisonoricFingering methods:


u_fingering = UnisonoricFingering(
    u_layout,
    [[False, False, True],
     [True, False, False]],
    [[False, False, True],
     [True, False, False]])


def test_UnisonoricFingering_repr():
    r = repr(u_fingering)
    assert "UnisonoricFingering(UnisonoricLayout([[Pitch(value=48, name='C4')" in r
    assert "[[False, False, True], [True, False, False]], "\
        "[[False, False, True], [True, False, False]])" in r


def test_UnisonoricFingering_str():
    assert str(u_fingering) == \
        '--- --- G4      --- --- G5 \n' \
        'G4  --- ---     G5  --- ---'


# Test BisonoricFingering methods:


b_fingering = BisonoricFingering(Direction.PUSH, u_fingering)


def test_BisonoricFingering_repr():
    assert 'BisonoricFingering(Direction.PUSH, UnisonoricFingering(UnisonoricLayout(' \
        in repr(b_fingering)


def test_BisonoricFingering_str():
    assert str(b_fingering) == \
        'PUSH:\n' \
        '--- --- G4      --- --- G5 \n' \
        'G4  --- ---     G5  --- ---'