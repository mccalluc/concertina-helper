#!/usr/bin/env python3

import argparse
from pathlib import Path
from signal import signal, SIGPIPE, SIG_DFL
from enum import Enum
from collections.abc import Callable

from pyabc2 import Tune

from concertina_helper.layouts.layout_loader import (
    list_layout_names, load_bisonoric_layout_by_path, load_bisonoric_layout_by_name)
from concertina_helper.layouts.bisonoric import BisonoricLayout, Direction
from concertina_helper.tune_on_layout import TuneOnLayout
from concertina_helper.penalties import (
    PenaltyFunction,
    penalize_bellows_change,
    penalize_finger_in_same_column,
    penalize_pull_at_start_of_measure)
from concertina_helper.type_defs import PitchToStr


class Format(Enum):
    def __init__(
        self,
        doc: str,
        button_down_f: PitchToStr,
        button_up_f: PitchToStr,
        direction_f: Callable[[Direction], str]
    ):
        self.doc = doc
        self.button_down_f = button_down_f
        self.button_up_f = button_up_f
        self.direction_f = direction_f
    # Enums are usually all caps, but these will come from the user.
    unicode = (
        'uses "○" and "●" to represent button state',
        lambda pitch: '●',
        lambda pitch: '○',
        lambda direction: direction.name
    )
    ascii = (
        'uses "." and "@" to represent button state',
        lambda pitch: '@',
        lambda pitch: '.',
        lambda direction: direction.name
    )
    long = (
        'spells out the names of pressed buttons',
        lambda pitch: str(pitch).ljust(4),
        lambda pitch: '--- ',
        lambda direction: direction.name
    )


def _parse_and_print_fingerings() -> None:
    '''
    Parses command line arguments, finds optimal fingering for tune, and prints.
    '''
    # Ignore broken pipes, so piping output to "head" will not error.
    # https://stackoverflow.com/a/30091579
    signal(SIGPIPE, SIG_DFL)

    parser = argparse.ArgumentParser(
        description='''
Given a file containing ABC notation,
and a concertina type,
prints possible fingerings.
''')
    parser.add_argument(
        'abc_path', type=Path,
        help='Path of ABC file')
    parser.add_argument(
        '--format', choices=[f.name for f in Format],
        default=Format.long.name,
        help='Output format. ' + ' / '.join(f'"{f.name}" {f.doc}' for f in Format))
    parser.add_argument(
        '--layout_transpose', default=0, type=int, metavar='SEMITONES',
        help='Semitones to transpose the layout; Negative transposes down')

    layout_group = parser.add_mutually_exclusive_group(required=True)
    layout_group.add_argument(
        '--layout_path', type=Path, metavar='PATH',
        help='Path of YAML file with concertina layout')
    layout_group.add_argument(
        '--layout_name', choices=list_layout_names(),
        help='Name of concertina layout')

    parser.add_argument(
        '--bellows_change_cost', type=float,
        metavar='N', default=2,
        help=penalize_bellows_change.__doc__)
    parser.add_argument(
        '--finger_in_same_column_cost', type=float,
        metavar='N', default=5,
        help=penalize_finger_in_same_column.__doc__)
    parser.add_argument(
        '--pull_at_start_of_measure_cost', type=float,
        metavar='N', default=0.5,
        help=penalize_pull_at_start_of_measure.__doc__)

    args = parser.parse_args()

    layout = (
        load_bisonoric_layout_by_path(args.layout_path)
        if args.layout_path else
        load_bisonoric_layout_by_name(args.layout_name)
    ).transpose(args.layout_transpose)
    abc_str = args.abc_path.read_text()
    penalty_functions = [
        penalize_bellows_change(args.bellows_change_cost),
        penalize_finger_in_same_column(args.finger_in_same_column_cost),
        penalize_pull_at_start_of_measure(args.pull_at_start_of_measure_cost)
    ]
    format = Format[args.format]

    print_fingerings(
        abc_str, layout,
        button_down_f=format.button_down_f,
        button_up_f=format.button_up_f,
        direction_f=format.direction_f,
        penalty_functions=penalty_functions)


def print_fingerings(
    abc_str: str,
    layout: BisonoricLayout,
    button_down_f: PitchToStr = lambda _: '@',
    button_up_f: PitchToStr = lambda _: '.',
    direction_f: Callable[[Direction], str] = lambda direction: direction.name,
    penalty_functions: list[PenaltyFunction] = []
) -> None:
    '''
    The core of the CLI functionality.
    - `abc_str`: A multiline string containing ABC notation.
    - `layout`: A bisonoric layout, either built-in or supplied by user.
    - `button_down_f`, `button_up_f`, `direction_f`: Functions that determine output style.
    - `penalty_functions`: Heuristic functions that define what makes a good fingering.
    '''
    if not penalty_functions:
        raise ValueError('At least one penalty function must be provided')
    tune = Tune(abc_str)
    t_l = TuneOnLayout(tune, layout)

    for annotated_fingering in t_l.get_best_fingerings(penalty_functions):
        print(f'Measure {annotated_fingering.measure}')
        print(annotated_fingering.fingering.format(
            button_down_f=button_down_f,
            button_up_f=button_up_f,
            direction_f=direction_f
        ))
