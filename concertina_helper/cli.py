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
from .note_generators import notes_from_tune, notes_from_pitches
from .penalties import (
    PenaltyFunction,
    penalize_bellows_change,
    penalize_finger_in_same_column,
    penalize_pull_at_start_of_measure,
    penalize_outer_fingers)
from .type_defs import Direction, PitchToStr, Annotation
from .output_utils import condense


class _OutputFormat(Enum):
    def __init__(
        self,
        doc: str,
        button_down_f: PitchToStr | None = None,
        button_up_f: PitchToStr | None = None,
        direction_f: Callable[[Direction], str] | None = None
    ):
        self.doc = doc
        self.button_down_f = button_down_f
        self.button_up_f = button_up_f
        self.direction_f = direction_f
    UNICODE = (
        'uses "○" and "●" to represent button state',
        lambda pitch: '● ',
        lambda pitch: '○ ',
        lambda direction: (
            f'-> {direction.name} <-'
            if direction == Direction.PUSH
            else f'<- {direction.name} ->')
    )
    ASCII = (
        'uses "." and "@" to represent button state',
        lambda pitch: '@',
        lambda pitch: '.',
        lambda direction: direction.name
    )
    LONG = (
        'spells out the names of pressed buttons',
        lambda pitch: str(pitch).ljust(4),
        lambda pitch: '--- ',
        lambda direction: direction.name
    )
    COMPACT = (
        'multiple fingerings represented in single grid'
    )


def _format_enum(enum: Iterable) -> str:
    return ' / '.join(f'"{opt.name}" {opt.doc}' for opt in enum)  # type: ignore


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
        'input', type=Path,
        help='Input file: Parsed either as a list of pitches, one per line, '
        'or as ABC, if the first lines starts with "X:".')
    parser.add_argument(
        '--output_format', choices=[f.name for f in _OutputFormat],
        default=_OutputFormat.LONG.name,
        help='Output format. ' + _format_enum(_OutputFormat))

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

    input_text = args.input.read_text()
    notes = (
        notes_from_tune(Tune(input_text))
        if input_text.startswith('X:') else
        notes_from_pitches(input_text.split('\n'))
    )

    layout = (
        load_bisonoric_layout_by_path(args.layout_path)
        if args.layout_path else
        load_bisonoric_layout_by_name(args.layout_name)
    ).transpose(args.layout_transpose)

    penalty_functions = [] if args.show_all else [
        penalize_bellows_change(args.bellows_change_cost),
        penalize_finger_in_same_column(args.finger_in_same_column_cost),
        penalize_pull_at_start_of_measure(args.pull_at_start_of_measure_cost),
        penalize_outer_fingers(args.outer_fingers_cost)
    ]
    output_format = _OutputFormat[args.output_format]

    print_fingerings(
        notes, layout,
        button_down_f=output_format.button_down_f,
        button_up_f=output_format.button_up_f,
        direction_f=output_format.direction_f,
        penalty_functions=penalty_functions)


def print_fingerings(
    notes: Iterable[Annotation],
    layout: BisonoricLayout,
    button_down_f: PitchToStr | None = lambda _: '@',
    button_up_f: PitchToStr | None = lambda _: '.',
    direction_f: Callable[[Direction], str] | None = lambda direction: direction.name,
    penalty_functions: Iterable[PenaltyFunction] = []
) -> None:
    '''
    The core of the CLI functionality.
    - `notes`: A sequence of annotated pitches.
    - `layout`: A bisonoric layout, either built-in or supplied by user.
    - `button_down_f`, `button_up_f`, `direction_f`:
      Functions that determine output style.
    - `penalty_functions`: Heuristic functions that define what makes a good fingering.
      If empty, all fingerings will be printed.
    '''
    n_l = NotesOnLayout(notes, layout)

    if penalty_functions:
        best = n_l.get_best_fingerings(penalty_functions)
        if direction_f is None:
            # TODO: split on measures?
            print(condense(best))
        else:
            assert (
                button_down_f is not None
                and button_up_f is not None
                and direction_f is not None), 'Either set all or none'
            for annotated_fingering in best:
                print(annotated_fingering.format(
                    button_down_f=button_down_f,
                    button_up_f=button_up_f,
                    direction_f=direction_f))
    else:
        if direction_f is None:
            raise ValueError('Display functions required to show all fingerings')
        assert (
            button_down_f is not None
            and button_up_f is not None
            and direction_f is not None), 'Either set all or none'
        for annotation, annotated_fingering_set in n_l.get_all_fingerings():
            if not annotated_fingering_set:
                a = annotation
                print(f'No fingerings for {a.pitch} in measure {a.measure}')
                continue
            for annotated_fingering in annotated_fingering_set:
                print(annotated_fingering.format(
                    button_down_f=button_down_f,
                    button_up_f=button_up_f,
                    direction_f=direction_f))
