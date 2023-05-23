from collections.abc import Callable

from .type_defs import Direction

from .layouts.bisonoric import (
    AnnotatedBisonoricFingering, BisonoricFingering)


PenaltyFunction = Callable[[
    AnnotatedBisonoricFingering, AnnotatedBisonoricFingering], float]

# TODO: Penalize outer columns?
# TODO: Penalize top row?


def penalize_bellows_change(cost: float) -> PenaltyFunction:
    '''
    Penalize fingerings where the bellows changes direction between notes
    '''
    def calculate(
            f1: AnnotatedBisonoricFingering,
            f2: AnnotatedBisonoricFingering) -> float:
        return cost if f1.fingering.direction != f2.fingering.direction else 0
    return calculate


def penalize_finger_in_same_column(cost: float) -> PenaltyFunction:
    '''
    Penalize fingerings where one finger changes rows between notes
    '''
    def calculate(
            f1: AnnotatedBisonoricFingering,
            f2: AnnotatedBisonoricFingering) -> float:
        '''
        This assumes fingers should be moving between notes: It will need to change
        if this is extended to cover sustained bass notes under a melody.
        '''
        return (
            cost if _find_columns_used(f1.fingering) ==
            _find_columns_used(f2.fingering)
            else 0)
    return calculate


def penalize_outer_fingers(cost: float) -> PenaltyFunction:
    '''
    Penalize fingerings that use outer fingers of either hand instead of inner.
    This is useful as a tiebreaker.
    '''
    def calculate(
            f1: AnnotatedBisonoricFingering,
            f2: AnnotatedBisonoricFingering) -> float:
        return cost * sum(1 / abs(i) for i in _find_columns_used(f2.fingering))
    return calculate


def penalize_pull_at_start_of_measure(cost: float) -> PenaltyFunction:
    '''
    Penalize fingerings where a pull begins a measure;
    Hitting the downbeat with a push can be more musical.'''
    def calculate(
            f1: AnnotatedBisonoricFingering,
            f2: AnnotatedBisonoricFingering) -> float:
        return cost if f2.fingering.direction == Direction.PULL else 0
    return calculate


def _find_columns_used(fingering: BisonoricFingering) -> set[int]:
    '''
    Returns a set of integers representing the buttons used.
    - On the left: 1 2 3 4 5
    - On the right: -5 -4 -3 -2 -1

    Taking the inverse of the absolute value gives us a number
    which is small for the inner fingers, but larger for the pinkies.

    This is used in `penalize_outer_fingers`.
    '''
    used = set()
    for row in fingering.left_mask:
        for i, button in enumerate(reversed(row)):
            if button:
                used.add(i+1)
    for row in fingering.right_mask:
        for i, button in enumerate(row):
            if button:
                used.add(-(i+1))
    return used
