from __future__ import annotations
from abc import ABC, abstractmethod
from collections.abc import Generator, Iterable

from pyabc2 import Tune

from .type_defs import Annotation, Pitch


def notes_from_tune(tune: Tune) -> Generator[Annotation]:
    for i, measure in enumerate(tune.measures):
        for note in measure:
            yield Annotation(
                measure=i + 1,
                pitch=Pitch(note.to_pitch().name)
            )


def notes_from_pitches(pitch_names: Iterable[str]) -> Generator[Annotation]:
    measure = 1
    for name in pitch_names:
        yield Annotation(
            measure=measure,
            pitch=Pitch(name.strip())
        )
