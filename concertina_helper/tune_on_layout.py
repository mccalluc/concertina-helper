from __future__ import annotations
from dataclasses import dataclass
from itertools import chain

from .layouts import BisonoricLayout, BisonoricFingering
from .finger_finder import find_best_fingerings

from pyabc2 import Tune


@dataclass
class TuneOnLayout:
    tune: Tune
    layout: BisonoricLayout

    def get_all_fingerings(self) -> list[set[BisonoricFingering]]:
        return list(chain(*[
            [self.layout.get_fingerings(note.to_pitch()) for note in measure]
            for measure in self.tune.measures
        ]))

    def get_best_fingerings(self) -> list[BisonoricFingering]:
        return find_best_fingerings(self.get_all_fingerings())
