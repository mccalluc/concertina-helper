from pathlib import Path
import re

from yaml import safe_load

from ..type_defs import PitchProxy, PitchProxyMatrix
from .bisonoric import BisonoricLayout
from .unisonoric import UnisonoricLayout


def _names_to_pitches(matrix: list[list[str]]) -> PitchProxyMatrix:
    '''
    >>> pitch_matrix = _names_to_pitches([['C4']])
    >>> pitch_matrix[0][0].name
    'C4'
    '''
    return PitchProxyMatrix(tuple(tuple(PitchProxy(name) for name in row) for row in matrix))


def _parse_matrix(rows: list[str]) -> PitchProxyMatrix:
    '''
    >>> pitch_matrix = _parse_matrix(['C4 E4 G4'])
    >>> pitch_matrix[0][0].name
    'C4'
    '''
    return _names_to_pitches([re.split(r'\s+', row.strip()) for row in rows])


def _parse_unisonoric_layout(layout_spec: dict) -> UnisonoricLayout:
    left_matrix = _parse_matrix(layout_spec['left'])
    right_matrix = _parse_matrix(layout_spec['right'])
    return UnisonoricLayout(left_matrix, right_matrix)


def _parse_bisonoric_layout(layout_spec: dict) -> BisonoricLayout:
    push_layout = _parse_unisonoric_layout(layout_spec['push'])
    pull_layout = _parse_unisonoric_layout(layout_spec['pull'])
    return BisonoricLayout(push_layout=push_layout, pull_layout=pull_layout)


def load_bisonoric_layout_by_path(layout_path: Path) -> BisonoricLayout:
    layout_yaml = layout_path.read_text()
    layout_spec = safe_load(layout_yaml)
    return _parse_bisonoric_layout(layout_spec)


def load_bisonoric_layout_by_name(layout_name: str) -> BisonoricLayout:
    if not re.fullmatch(r'\w+', layout_name):
        raise ValueError('invalid layout name')
    layout_path = Path(__file__).parent / f'{layout_name}.yaml'
    return load_bisonoric_layout_by_path(layout_path)


def list_layout_names() -> list[str]:
    '''
    >>> list_layout_names()
    ['wheatstone_cg']
    '''
    return [path.stem for path in Path(__file__).parent.glob('*.yaml')]


# TODO: Add a test and uncomment.
# def load_unisonoric_layout_by_path(layout_path: Path) -> UnisonoricLayout:
#     layout_yaml = layout_path.read_text()
#     layout_spec = safe_load(layout_yaml)
#     return _parse_unisonoric_layout(layout_spec)
