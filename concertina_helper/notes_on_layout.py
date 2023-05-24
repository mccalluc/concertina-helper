from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Iterable

from .layouts.bisonoric import BisonoricLayout, AnnotatedBisonoricFingering
from .finger_finder import find_best_fingerings
from .penalties import PenaltyFunction
from .type_defs import Annotation


@dataclass
class NotesOnLayout:
    '''
    Represents a sequence of notes on a particular layout
    '''
    notes: Iterable[Annotation]
    layout: BisonoricLayout

    def get_all_fingerings(self) -> \
            Iterable[tuple[Annotation, set[AnnotatedBisonoricFingering]]]:
        '''
        For each note in the tune, returns all possible fingerings.
        '''
        return [
            (
                annotation,
                {
                    AnnotatedBisonoricFingering(
                        fingering=f,
                        annotation=annotation)
                    for f in self.layout.get_fingerings(annotation.pitch)
                }
            )
            for annotation in self.notes
        ]

    def get_best_fingerings(self, penalty_functions: Iterable[PenaltyFunction]) \
            -> Iterable[AnnotatedBisonoricFingering]:
        '''
        Returns a list of fingerings that minimizes the cost for the entire tune,
        as measured by the provided `penalty_functions`.
        '''
        f_sets = []
        for annotation, f_set in self.get_all_fingerings():
            if not f_set:
                a = annotation
                raise ValueError(f'No fingerings for {a.pitch} in measure {a.measure}')
            f_sets.append(f_set)
        return find_best_fingerings(f_sets, penalty_functions)
