import argparse
from pathlib import Path
from signal import signal, SIGPIPE, SIG_DFL
from enum import Enum
from collections.abc import Callable, Iterable

from pyabc2 import Tune

from .layouts.layout_loader import (
    list_layout_names, load_bisonoric_layout_by_path, load_bisonoric_layout_by_name)
from .layouts.bisonoric import BisonoricLayout
from .notes_on_layout import NotesOnLayout
from .note_generators import notes_from_tune
from .penalties import (
    PenaltyFunction,
    penalize_bellows_change,
    penalize_finger_in_same_column,
    penalize_pull_at_start_of_measure)
from .type_defs import Direction, PitchToStr


class _Format(Enum):
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
        lambda pitch: '● ',
        lambda pitch: '○ ',
        lambda direction: (
            f'-> {direction.name} <-'
            if direction == Direction.PUSH
            else f'<- {direction.name} ->')
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
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='''
Given a file containing ABC notation,
and a concertina type,
prints possible fingerings.
''')
    parser.add_argument(
        'abc_path', type=Path,
        help='Path of ABC file')
    parser.add_argument(
        '--format', choices=[f.name for f in _Format],
        default=_Format.long.name,
        help='Output format. ' + ' / '.join(f'"{f.name}" {f.doc}' for f in _Format))

    layout_group = parser.add_argument_group(
        'Layout options',
        'Supply your own layout, or use a predefined one, optionally transposed\n')
    layout_source_group = layout_group.add_mutually_exclusive_group(required=True)
    layout_source_group.add_argument(
        '--layout_path', type=Path, metavar='PATH',
        help='Path of YAML file with concertina layout')
    layout_source_group.add_argument(
        '--layout_name', choices=list_layout_names(),
        help='Name of concertina layout')
    layout_group.add_argument(
        '--layout_transpose', default=0, type=int, metavar='SEMITONES',
        help='Semitones to transpose the layout; Negative transposes down')

    cost_group = parser.add_argument_group(
        'Cost options',
        'Configure the relative costs of different transitions between fingerings\n')
    for name in globals():
        if name.startswith('penalize_'):
            param_name = name.replace('penalize_', '') + '_cost'
            cost_group.add_argument(
                f'--{param_name}', type=float,
                metavar='N', default=1,
                help=globals()[name].__doc__)
    cost_group.add_argument(
        '--show_all', action='store_true',
        help='Ignore cost options and just show all possible fingerings')

    args = parser.parse_args()

    layout = (
        load_bisonoric_layout_by_path(args.layout_path)
        if args.layout_path else
        load_bisonoric_layout_by_name(args.layout_name)
    ).transpose(args.layout_transpose)
    abc_str = args.abc_path.read_text()
    penalty_functions = [] if args.show_all else [
        penalize_bellows_change(args.bellows_change_cost),
        penalize_finger_in_same_column(args.finger_in_same_column_cost),
        penalize_pull_at_start_of_measure(args.pull_at_start_of_measure_cost)
    ]
    format = _Format[args.format]

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
    penalty_functions: Iterable[PenaltyFunction] = []
) -> None:
    '''
    The core of the CLI functionality.
    - `abc_str`: A multiline string containing ABC notation.
    - `layout`: A bisonoric layout, either built-in or supplied by user.
    - `button_down_f`, `button_up_f`, `direction_f`:
      Functions that determine output style.
    - `penalty_functions`: Heuristic functions that define what makes a good fingering.
      If empty, all fingerings will be printed.
    '''
    tune = Tune(abc_str)
    t_l = NotesOnLayout(notes_from_tune(tune), layout)

    if penalty_functions:
        for annotated_fingering in t_l.get_best_fingerings(penalty_functions):
            print(annotated_fingering.format(
                button_down_f=button_down_f,
                button_up_f=button_up_f,
                direction_f=direction_f))
    else:
        for annotation, annotated_fingering_set in t_l.get_all_fingerings():
            if not annotated_fingering_set:
                a = annotation
                print(f'No fingerings for {a.pitch} in measure {a.measure}')
                continue
            for annotated_fingering in annotated_fingering_set:
                print(annotated_fingering.format(
                    button_down_f=button_down_f,
                    button_up_f=button_up_f,
                    direction_f=direction_f))
