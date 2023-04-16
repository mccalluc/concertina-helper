from layouts import UnisonoricLayout, UnisonoricFingering, _names_to_pitches

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

u_fingering = UnisonoricFingering(
    u_layout,
    [[False, False, True],
     [True, False, False]],
    [[False, False, True],
     [True, False, False]])

def test_UnisonoricFingering_repr():
    r = repr(u_fingering)
    assert "UnisonoricFingering(UnisonoricLayout([[Pitch(value=48, name='C4')" in r
    assert "[[False, False, True], [True, False, False]], [[False, False, True], [True, False, False]])" in r

def test_UnisonoricFingering_str():
    assert str(u_fingering) == \
    '--- --- G4      --- --- G5 \n' \
    'G4  --- ---     G5  --- ---'