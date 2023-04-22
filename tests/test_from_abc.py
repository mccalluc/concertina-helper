from pathlib import Path

from from_abc import get_best_fingerings


path = Path('tests/cherrytree.abc')


def test_get_fingerings_default():
    get_best_fingerings(path)
    # TODO
