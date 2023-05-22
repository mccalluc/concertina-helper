from __future__ import annotations
from collections.abc import Iterable

from pyabc2 import Tune

from .type_defs import Annotation, Pitch


def notes_from_tune(tune: Tune) -> Iterable[Annotation]:
    for i, measure in enumerate(tune.measures):
        for note in measure:
            yield Annotation(
                measure=i + 1,
                pitch=Pitch(note.to_pitch().name)
            )


def notes_from_pitches(pitch_names: Iterable[str]) -> Iterable[Annotation]:
    for name in pitch_names:
        yield Annotation(
            measure=1,
            pitch=Pitch(name.strip())
        )
