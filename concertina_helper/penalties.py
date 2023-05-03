from collections.abc import Callable

from .layouts.bisonoric import (
    AnnotatedBisonoricFingering, BisonoricFingering, Direction)


PenaltyFunction = Callable[[
    AnnotatedBisonoricFingering, AnnotatedBisonoricFingering], float]

# TODO: Penalize outer columns?
# TODO: Penalize top row?


def penalize_bellows_change(cost: float) -> PenaltyFunction:
    def calculate(
            f1: AnnotatedBisonoricFingering,
            f2: AnnotatedBisonoricFingering) -> float:
        return cost if f1.fingering.direction != f2.fingering.direction else 0
    return calculate


def penalize_finger_in_same_column(cost: float) -> PenaltyFunction:
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


def penalize_pull_at_start_of_measure(cost: float) -> PenaltyFunction:
    def calculate(
            f1: AnnotatedBisonoricFingering,
            f2: AnnotatedBisonoricFingering) -> float:
        return cost if f2.fingering.direction == Direction.PULL else 0
    return calculate


def _find_columns_used(fingering: BisonoricFingering) -> set[int]:
    used = set()
    # TODO: Make this a method.
    for row in fingering.left_mask:
        for i, button in enumerate(reversed(row)):
            if button:
                used.add(-(i+1))
    for row in fingering.right_mask:
        for i, button in enumerate(row):
            if button:
                used.add(i+1)
    return used
