#!/usr/bin/env python3

import argparse
from pathlib import Path
from textwrap import indent
from signal import signal, SIGPIPE, SIG_DFL

from pyabc2 import Tune

from .layouts import cg_anglo_wheatstone_layout

# Ignore broken pipes, so piping output to "head" will not error.
# https://stackoverflow.com/a/30091579
signal(SIGPIPE, SIG_DFL)


def main():
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
    path = Path(args.abc)
    tune = Tune(path.read_text())
    verbose = args.verbose
    print_fingerings(tune, verbose)


def print_fingerings(tune: Tune, verbose: bool):
    for i, measure in enumerate(tune.measures):
        print(f'Measure {i + 1}')
        for note in measure:
            pitch = note.to_pitch()
            print(indent(pitch.name, ' '*2))
            fingerings = cg_anglo_wheatstone_layout.get_fingerings(pitch)
            for f in fingerings:
                print(indent(str(f) if verbose else f.format(), ' '*4))
