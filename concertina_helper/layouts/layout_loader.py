from pathlib import Path
from collections.abc import Iterable

import re

from yaml import safe_load

from ..type_defs import Pitch, PitchMatrix
from .bisonoric import BisonoricLayout
from .unisonoric import UnisonoricLayout


def _names_to_pitches(matrix: Iterable[Iterable[str]]) -> PitchMatrix:
    '''
    >>> pitch_matrix = _names_to_pitches([['C4']])
    >>> print(pitch_matrix[0][0])
    C4
    '''
    return PitchMatrix(
        tuple(
            tuple(
                Pitch(name) for name in row
            ) for row in matrix
        )
    )


def _parse_matrix(rows: Iterable[str]) -> PitchMatrix:
    '''
    >>> pitch_matrix = _parse_matrix(['C4 E4 G4'])
    >>> print(pitch_matrix[0][0])
    C4
    '''
    return _names_to_pitches([re.split(r'\s+', row.strip()) for row in rows])


def parse_unisonoric_layout(layout_spec: dict) -> UnisonoricLayout:
    left_matrix = _parse_matrix(layout_spec['left'])
    right_matrix = _parse_matrix(layout_spec['right'])
    return UnisonoricLayout(left_matrix, right_matrix)


def parse_bisonoric_layout(layout_spec: dict) -> BisonoricLayout:
    push_layout = parse_unisonoric_layout(layout_spec['push'])
    pull_layout = parse_unisonoric_layout(layout_spec['pull'])
    return BisonoricLayout(push_layout=push_layout, pull_layout=pull_layout)


def load_bisonoric_layout_by_path(layout_path: Path) -> BisonoricLayout:
    '''
    Expects the file at `layout_path` to be YAML, with a structure like this:
    ```
    push:
        left:
            - C3 G3 C4  E4 G4
            - B3 D4 G4  B4 D5
        right:
            - C5  E5 G5  C6  E6
            - G5  B5 D6  G6  B6
    pull:
        left:
            - G3 B3  D4  F4 A4
            - A3 F#4 A4  C5 E5
        right:
            - B4  D5 F5  A5  B5
            - F#5 A5 C6  E6  F#6
    ```
    - `push` and `pull` at the top level.
    - `left` and `right` inside.
    - Each contains a list of strings, representing rows of buttons.
    - The strings are the pitches of that row of keys, space delimitted.
    '''
    layout_yaml = layout_path.read_text()
    layout_spec = safe_load(layout_yaml)
    return parse_bisonoric_layout(layout_spec)


def load_bisonoric_layout_by_name(layout_name: str) -> BisonoricLayout:
    '''
    The `layout_name` must be one of the names returned by `list_layout_names()`.
    '''
    if not re.fullmatch(r'\w+', layout_name):
        raise ValueError('invalid layout name')
    layout_path = Path(__file__).parent / f'{layout_name}.yaml'
    return load_bisonoric_layout_by_path(layout_path)


def list_layout_names() -> Iterable[str]:
    '''
    Lists all preconfigured layouts. To change the key of a layout, use
    `concertina_helper.layouts.bisonoric.BisonoricLayout.transpose`.

    >>> list_layout_names()
    ['20_cg', '30_jefferies_cg', '30_wheatstone_cg']
    '''
    return sorted([path.stem for path in Path(__file__).parent.glob('*.yaml')])


# TODO: Add a test and uncomment.
# def load_unisonoric_layout_by_path(layout_path: Path) -> UnisonoricLayout:
#     layout_yaml = layout_path.read_text()
#     layout_spec = safe_load(layout_yaml)
#     return _parse_unisonoric_layout(layout_spec)
