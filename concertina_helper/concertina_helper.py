#!/usr/bin/env python3

import argparse
from pathlib import Path
import sys
from textwrap import indent

from pyabc2 import Tune, Note

from .layouts import cg_anglo_wheatstone_layout

def main():
    parser = argparse.ArgumentParser(
        description='''
Given a file containing ABC notation,
and a concertina type,
prints suggested fingerings.
''')
    parser.add_argument(
        '--abc', type=Path, required=True,
        help='Path of ABC file')
    parser.add_argument(
        '--layout', choices=['Wheatstone'], default='Wheatstone')
    parser.add_argument(
        '--key', choices=['CG'], default='CG')

    args = parser.parse_args()
    path = Path(args.abc)
    tune = Tune(path.read_text())
    print_fingerings(tune)
    return 0


def print_fingerings(tune: Tune):
    for i, measure in enumerate(tune.measures):
        print(f'Measure {i + 1}')
        for note in measure:
            pitch = note.to_pitch()
            print(indent(pitch.name, ' '*2))
            fingerings = cg_anglo_wheatstone_layout.get_fingerings(pitch)
            for f in fingerings:
                print(indent(str(f), ' '*4))


if __name__ == "__main__":
    exit_status = main()
    sys.exit(exit_status)
