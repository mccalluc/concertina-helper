from pathlib import Path

from from_abc import get_fingerings


path = Path('tests/cherrytree.abc')


def test_get_fingerings_default():
    lines = get_fingerings(path, False).split('\n')[0:10]
    assert 'Measure 1' in lines
    assert '  G4' in lines
    assert '    .....   .....' in lines


def test_get_fingerings_verbose():
    lines = get_fingerings(path, True).split('\n')[0:10]
    assert 'Measure 1' in lines
    assert '  G4' in lines
    assert '    --- --- --- --- ---    --- --- --- --- --- ' in lines
