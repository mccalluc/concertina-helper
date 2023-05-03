#!/usr/bin/env python3

import argparse
from pathlib import Path
from signal import signal, SIGPIPE, SIG_DFL

from pyabc2 import Tune

from concertina_helper.layouts.layout_loader import (
    list_layout_names, load_bisonoric_layout_by_path, load_bisonoric_layout_by_name)
from concertina_helper.layouts.bisonoric import BisonoricLayout
from concertina_helper.tune_on_layout import TuneOnLayout
from concertina_helper.penalties import (
    PenaltyFunction,
    penalize_bellows_change,
    penalize_finger_in_same_column,
    penalize_pull_at_start_of_measure)


def _from_abc() -> None:  # pragma: no cover
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
        '--verbose', action='store_true')
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
    from_abc(
        abc_str, layout,
        is_verbose=args.verbose,
        penalty_functions=penalty_functions)


def from_abc(
    abc_str: str,
    layout: BisonoricLayout,
    is_verbose: bool = False,
    penalty_functions: list[PenaltyFunction] = []
) -> None:  # pragma: no cover
    '''
    The core of the CLI functionality.
    - `abc_str`: A multiline string containing ABC notation.
    - `layout`: A bisonoric layout, either built-in or supplied by user.
    - `is_verbose`: Should the output show notes, or just whether buttons are down?
    - `penalty_functions`: Encapsulate heuristics about what makes a good fingering.
    '''
    tune = Tune(abc_str)
    t_l = TuneOnLayout(tune, layout)

    for annotated_fingering in t_l.get_best_fingerings(penalty_functions):
        print(f'Measure {annotated_fingering.measure}')
        if is_verbose:
            print(str(annotated_fingering.fingering))
        else:
            print(annotated_fingering.fingering.format())
