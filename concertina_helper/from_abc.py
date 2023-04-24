#!/usr/bin/env python3

import argparse
from pathlib import Path
from signal import signal, SIGPIPE, SIG_DFL

from pyabc2 import Tune

from concertina_helper.bisonoric import cg_anglo_wheatstone_layout
from concertina_helper.tune_on_layout import TuneOnLayout


def main() -> None:  # pragma: no cover
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
        'abc', type=Path,
        help='Path of ABC file')
    parser.add_argument(
        '--layout', choices=['Wheatstone'], default='Wheatstone')
    parser.add_argument(
        '--key', choices=['CG'], default='CG')
    parser.add_argument(
        '--verbose', action='store_true'
    )

    args = parser.parse_args()

    tune = Tune(args.abc.read_text())
    layout = cg_anglo_wheatstone_layout
    t_l = TuneOnLayout(tune, layout)
    for annotated_fingering in t_l.get_best_fingerings():
        print(f'Measure {annotated_fingering.measure}')
        if args.verbose:
            print(str(annotated_fingering.fingering))
        else:
            print(annotated_fingering.fingering.format())
