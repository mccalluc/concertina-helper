from __future__ import annotations
from dataclasses import dataclass
from itertools import chain

from .layouts.bisonoric import BisonoricLayout, AnnotatedBisonoricFingering
from .finger_finder import find_best_fingerings
from .penalties import PenaltyFunction

from pyabc2 import Tune


@dataclass
class TuneOnLayout:
    '''
    Represents a particular tune on a particular layout
    '''
    tune: Tune
    layout: BisonoricLayout

    def get_all_fingerings(self) -> list[set[AnnotatedBisonoricFingering]]:
        '''
        For each note in the tune, returns all possible fingerings.
        '''
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

    def get_best_fingerings(self, penalty_functions: list[PenaltyFunction]) \
            -> list[AnnotatedBisonoricFingering]:
        '''
        Returns a list of fingerings that minimizes the cost for the entire tune,
        as measured by the provided `penalty_functions`.
        '''
        return find_best_fingerings(self.get_all_fingerings(), penalty_functions)
