#!/usr/bin/env python3

import argparse
from pathlib import Path
from signal import signal, SIGPIPE, SIG_DFL

from pyabc2 import Tune

from concertina_helper.layouts.layout_loader import (
    list_layout_names, load_bisonoric_layout_by_path, load_bisonoric_layout_by_name)
from concertina_helper.tune_on_layout import TuneOnLayout


def from_abc() -> None:  # pragma: no cover
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
        '--verbose', action='store_true'
    )

    layout_group = parser.add_mutually_exclusive_group(required=True)
    layout_group.add_argument(
        '--layout_path', type=Path,
        help='Path of YAML file with concertina layout')
    layout_group.add_argument(
        '--layout_name', choices=list_layout_names(),
        help='Name of concertina layout')

    args = parser.parse_args()

    if args.layout_path:
        layout = load_bisonoric_layout_by_path(args.layout_path)
    else:
        layout = load_bisonoric_layout_by_name(args.layout_name)

    tune = Tune(args.abc_path.read_text())
    t_l = TuneOnLayout(tune, layout)

    for annotated_fingering in t_l.get_best_fingerings():
        print(f'Measure {annotated_fingering.measure}')
        if args.verbose:
            print(str(annotated_fingering.fingering))
        else:
            print(annotated_fingering.fingering.format())
