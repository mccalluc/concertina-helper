from __future__ import annotations
from collections.abc import Iterable

from pyabc2 import Tune

from .type_defs import Annotation, Pitch


def notes_from_tune(tune: Tune) -> Iterable[Annotation]:
    '''
    Given a pyabc2 `Tune`,
    returns an iterable of the annotated pitches.

    >>> tune = Tune("""
    ... X: 1
    ... K: Cmaj
    ... CEG||
    ... """)
    >>> for note in notes_from_tune(tune):
    ...     print(note)
    Annotation(pitch=Pitch(name='C4'), measure=1)
    Annotation(pitch=Pitch(name='E4'), measure=1)
    Annotation(pitch=Pitch(name='G4'), measure=1)
    '''
    for i, measure in enumerate(tune.measures):
        for note in measure:
            yield Annotation(
                measure=i + 1,
                pitch=Pitch(note.to_pitch().name)
            )


def notes_from_pitches(pitch_names: Iterable[str]) -> Iterable[Annotation]:
    '''
    Given a sequence of scientific pitch names,
    strips padding and returns an iterable of the annotated pitches.

    >>> for note in notes_from_pitches(['C4', '  E4', 'G4  ']):
    ...     print(note)
    Annotation(pitch=Pitch(name='C4'), measure=1)
    Annotation(pitch=Pitch(name='E4'), measure=1)
    Annotation(pitch=Pitch(name='G4'), measure=1)
    '''
    for name in pitch_names:
        yield Annotation(
            measure=1,
            pitch=Pitch(name.strip())
        )
