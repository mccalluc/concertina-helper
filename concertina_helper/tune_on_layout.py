from __future__ import annotations
from dataclasses import dataclass
from itertools import chain

from .bisonoric import BisonoricLayout, AnnotatedBisonoricFingering
from .finger_finder import find_best_fingerings

from pyabc2 import Tune


@dataclass
class TuneOnLayout:
    tune: Tune
    layout: BisonoricLayout

    def get_all_fingerings(self) -> list[set[AnnotatedBisonoricFingering]]:
        return list(chain(*[
            [
                {
                    AnnotatedBisonoricFingering(fingering=f, measure=i + 1)
                    for f in self.layout.get_fingerings(note.to_pitch())
                }
                for note in measure
            ]
            for i, measure in enumerate(self.tune.measures)
        ]))

    def get_best_fingerings(self) -> list[AnnotatedBisonoricFingering]:
        return find_best_fingerings(self.get_all_fingerings())
