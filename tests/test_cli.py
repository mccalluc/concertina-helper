from pathlib import Path
from unittest.mock import patch

import pytest

from concertina_helper.cli import (_parse_and_print_fingerings, print_fingerings)
from concertina_helper.layouts.layout_loader import load_bisonoric_layout_by_name
from concertina_helper.penalties import penalize_bellows_change
from concertina_helper.note_generators import notes_from_pitches


def test_cli_help(capsys):  # pragma: no cover
    try:
        with patch('argparse._sys.argv', ['concertina-helper', '--help']):
            _parse_and_print_fingerings()
    except SystemExit:
        pass
    captured = capsys.readouterr().out
    assert 'usage: concertina-helper' in captured
    # We could read README.md and compare,
    # but the linewrapping is different than when you call it from the shell


def test_cli_missing_layout(capsys):   # pragma: no cover
    try:
        with patch('argparse._sys.argv', ['concertina-helper', 'fake']):
            _parse_and_print_fingerings()
    except SystemExit:
        pass
    captured = capsys.readouterr().err
    assert '--layout_path --layout_name is required' in captured


def test_cli_default_render(capsys):
    with patch('argparse._sys.argv',
               ['concertina-helper', str(Path(__file__).parent / 'g-major.txt'),
                '--layout_name', '30_wheatstone_cg']):
        _parse_and_print_fingerings()
    captured = capsys.readouterr().out
    assert 'Measure 1' in captured
    assert '--- --- --- --- ---' in captured


def test_cli_ascii_render(capsys):
    with patch('argparse._sys.argv',
               ['concertina-helper', str(Path(__file__).parent / 'g-major.txt'),
                '--layout_name', '30_wheatstone_cg',
                '--output_format', 'ASCII']):
        _parse_and_print_fingerings()
    captured = capsys.readouterr().out
    assert 'Measure 1' in captured
    assert '.....' in captured


def test_cli_unicode_render(capsys):
    with patch('argparse._sys.argv',
               ['concertina-helper', str(Path(__file__).parent / 'g-major.abc'),
                '--layout_name', '30_wheatstone_cg',
                '--output_format', 'UNICODE',
                '--input_format', 'ABC']):
        _parse_and_print_fingerings()
    captured = capsys.readouterr().out
    assert 'Measure 1' in captured
    assert '○ ○ ○ ○ ○' in captured


def test_cli_compact_render(capsys):
    with patch('argparse._sys.argv',
               ['concertina-helper', str(Path(__file__).parent / 'g-major.abc'),
                '--layout_name', '30_wheatstone_cg',
                '--output_format', 'COMPACT',
                '--input_format', 'ABC']):
        _parse_and_print_fingerings()
    captured = capsys.readouterr().out
    assert '➃ ➅ ➇ . .' in captured


def test_cli_compact_render_too_long_error():
    with patch('argparse._sys.argv',
               ['concertina-helper', str(Path(__file__).parent / 'amelia-chords.abc'),
                '--layout_name', '30_wheatstone_cg',
                '--output_format', 'COMPACT',
                '--input_format', 'ABC']):
        with pytest.raises(
                ValueError, match=r'Length of fingerings \(393\) greater than allowed \(20\)'):
            _parse_and_print_fingerings()


def test_cli_compact_render_show_all_error():
    with patch('argparse._sys.argv',
               ['concertina-helper', str(Path(__file__).parent / 'amelia-chords.abc'),
                '--layout_name', '30_wheatstone_cg',
                '--output_format', 'COMPACT',
                '--input_format', 'ABC',
                '--show_all']):
        with pytest.raises(
                ValueError, match=r'Display functions required to show all fingerings'):
            _parse_and_print_fingerings()


# Since this is reused between tests,
# save it into a list to avoid side-effects.
notes = list(notes_from_pitches(['G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F#5', 'G5']))


def test_no_format_functions(capsys):
    print_fingerings(
        notes,
        load_bisonoric_layout_by_name('30_wheatstone_cg'))
    captured = capsys.readouterr().out
    assert 'Measure 1' in captured
    assert '.....' in captured


def test_render_with_penalty(capsys):
    print_fingerings(
        notes,
        load_bisonoric_layout_by_name('30_wheatstone_cg'),
        penalty_functions=[penalize_bellows_change(1)])
    captured = capsys.readouterr().out
    assert 'Measure 1 - G4\n' in captured
    assert '.....' in captured
    assert 'No fingerings' not in captured


def test_render_with_penalty_out_of_range():
    with pytest.raises(ValueError, match=r'No fingerings for G4 in measure 1'):
        print_fingerings(
            notes,
            load_bisonoric_layout_by_name('30_wheatstone_cg').transpose(24),
            penalty_functions=[penalize_bellows_change(1)])


def test_render_without_penalty(capsys):
    print_fingerings(
        notes,
        load_bisonoric_layout_by_name('30_wheatstone_cg'))
    captured = capsys.readouterr().out
    assert 'Measure 1 - G4\n' in captured
    assert '.....' in captured
    assert 'No fingerings' not in captured


def test_render_without_penalty_out_of_range(capsys):
    print_fingerings(
        notes,
        load_bisonoric_layout_by_name('30_wheatstone_cg').transpose(-24))
    captured = capsys.readouterr().out
    assert 'Measure 1 - G4\n' in captured
    assert '.....' in captured
    assert 'No fingerings' in captured
