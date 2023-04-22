#!/usr/bin/env python3

import argparse
from pathlib import Path
from textwrap import indent
from itertools import chain
from signal import signal, SIGPIPE, SIG_DFL

from pyabc2 import Tune

from concertina_helper.layouts import cg_anglo_wheatstone_layout, BisonoricFingering
from concertina_helper.finger_finder import FingerFinder


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
    print(get_best_fingerings(path, verbose))


# TODO: Move both of these to a utils package, or maybe methods on a (Tune, Layout) dataclass.

def get_all_fingerings(tune: Tune) -> list[set[BisonoricFingering]]:
    layout = cg_anglo_wheatstone_layout
    return list(chain(*[[layout.get_fingerings(note.to_pitch()) for note in measure] for measure in tune.measures]))


def get_best_fingerings(path: Path, verbose: bool):
    tune = Tune(path.read_text())
    # TODO: Capture measure notation again... maybe a (measure, note) tuple?
    all_fingerings = get_all_fingerings(tune)
    ff = FingerFinder(all_fingerings)
    # TODO: Instead of picking an arbitrary start and stop, there should be a helper method on ff.
    start = list(all_fingerings[0])[0]
    goal = list(all_fingerings[-1])[0]
    best = ff.astar(start, goal)
    print(best[0])  # TODO
    print('???')
