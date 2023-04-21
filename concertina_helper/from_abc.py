#!/usr/bin/env python3

import argparse
from pathlib import Path
from textwrap import indent
from signal import signal, SIGPIPE, SIG_DFL

from pyabc2 import Tune

from concertina_helper.layouts import cg_anglo_wheatstone_layout


def main():  # pragma: no cover
    #
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
    path = Path(args.abc)

    verbose = args.verbose
    print(get_fingerings(path, verbose))


def get_fingerings(path: Path, verbose: bool):
    tune = Tune(path.read_text())
    lines = []
    for i, measure in enumerate(tune.measures):
        lines.append(f'Measure {i + 1}')
        for note in measure:
            pitch = note.to_pitch()
            lines.append(indent(pitch.name, ' '*2))
            fingerings = cg_anglo_wheatstone_layout.get_fingerings(pitch)
            for f in fingerings:
                lines.append(indent(str(f) if verbose else f.format(), ' '*4))
    return '\n'.join(lines)
