from pathlib import Path
from unittest.mock import patch

import pytest

from concertina_helper.cli import (_parse_and_print_fingerings, print_fingerings)
from concertina_helper.layouts.layout_loader import load_bisonoric_layout_by_name
from concertina_helper.penalties import penalize_bellows_change


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
               ['concertina-helper', str(Path(__file__).parent / 'g-major.abc'),
                '--layout_name', '30_wheatstone_cg']):
        _parse_and_print_fingerings()
    captured = capsys.readouterr().out
    assert 'Measure 1' in captured
    assert '--- --- --- --- ---' in captured


def test_cli_ascii_render(capsys):
    with patch('argparse._sys.argv',
               ['concertina-helper', str(Path(__file__).parent / 'g-major.abc'),
                '--layout_name', '30_wheatstone_cg', '--format', 'ascii']):
        _parse_and_print_fingerings()
    captured = capsys.readouterr().out
    assert 'Measure 1' in captured
    assert '.....' in captured


def test_cli_unicode_render(capsys):
    with patch('argparse._sys.argv',
               ['concertina-helper', str(Path(__file__).parent / 'g-major.abc'),
                '--layout_name', '30_wheatstone_cg', '--format', 'unicode']):
        _parse_and_print_fingerings()
    captured = capsys.readouterr().out
    assert 'Measure 1' in captured
    assert '○○○○○' in captured


abc = (Path(__file__).parent / 'g-major.abc').read_text()


def test_no_format_functions(capsys):
    print_fingerings(
        abc,
        load_bisonoric_layout_by_name('30_wheatstone_cg'))
    captured = capsys.readouterr().out
    assert 'Measure 1' in captured
    assert '.....' in captured


def test_default_render(capsys):
    print_fingerings(
        abc,
        load_bisonoric_layout_by_name('30_wheatstone_cg'),
        penalty_functions=[penalize_bellows_change(1)])
    captured = capsys.readouterr().out
    assert 'Measure 1' in captured
    assert '.....' in captured
