from typing import Iterable
from dataclasses import dataclass
from collections.abc import Callable

from astar import AStar  # type: ignore

from .layouts.bisonoric import AnnotatedBisonoricFingering, BisonoricFingering, Direction


PenaltyFunction = Callable[[
    AnnotatedBisonoricFingering, AnnotatedBisonoricFingering], float]

# TODO: Penalize outer columns?
# TODO: Penalize top row?


def penalize_bellows_change(
        f1: AnnotatedBisonoricFingering,
        f2: AnnotatedBisonoricFingering) -> float:
    return 1 if f1.fingering.direction != f2.fingering.direction else 0


def penalize_finger_in_same_column(
        f1: AnnotatedBisonoricFingering,
        f2: AnnotatedBisonoricFingering) -> float:
    '''
    This assumes fingers should be moving: It need to change
    if this is extended to cover sustained bass notes under a melody.
    '''
    return 1 if _find_columns_used(f1.fingering) == _find_columns_used(f2.fingering) else 0


def penalize_pull_at_start_of_measure(
        f1: AnnotatedBisonoricFingering,
        f2: AnnotatedBisonoricFingering) -> float:
    return 1 if f2.fingering.direction == Direction.PULL else 0
    

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


def find_best_fingerings(
    all_fingerings: list[set[AnnotatedBisonoricFingering]],
    penalty_functions: list[PenaltyFunction]
        = [penalize_bellows_change, penalize_finger_in_same_column, penalize_pull_at_start_of_measure]
) -> list[AnnotatedBisonoricFingering]:
    '''
    Given a list of sets of possible fingerings,
    returns a list representing the best fingerings.
    See `concertina_helper.tune_on_layout.TuneOnLayout.get_best_fingerings`
    for a convenience method that wraps this.
    '''
    finder = _FingerFinder(all_fingerings, penalty_functions)
    return finder.find()


@dataclass(frozen=True)
class _Node:
    position: int
    annotated_fingering: AnnotatedBisonoricFingering | None


class _FingerFinder(AStar):
    def __init__(
            self,
            fingerings: list[set[AnnotatedBisonoricFingering]],
            penalty_functions: list[PenaltyFunction]):
        self.penalty_functions = penalty_functions
        self.index: dict[int, set[_Node]] = {
            i: {_Node(i, f) for f in f_set}
            for i, f_set in enumerate(fingerings)
        }

    def find(self) -> list[AnnotatedBisonoricFingering]:
        start = _Node(-1, None)
        max_index = max(self.index.keys())
        goal = list(self.index[max_index])[0]
        # is_goal_reached() only checks position,
        # so I think we can use any final node.
        # ... but then why is the goal parameter needed on astar(start, goal)?

        return [
            node.annotated_fingering for node in self.astar(start, goal)
            if node.annotated_fingering is not None
        ]

    def heuristic_cost_estimate(self, current: _Node, goal: _Node) -> float:
        return goal.position - current.position

    def distance_between(self, n1: _Node, n2: _Node) -> float:
        # TODO: Make the weightings here configurable.
        distance = float(abs(n1.position - n2.position))
        assert distance == 1.0  # Should only be used with immediate neighbors

        if n1.annotated_fingering is not None and n2.annotated_fingering is not None:
            # If either is an end node, thers is no additional transition cost.
            f1 = n1.annotated_fingering
            f2 = n2.annotated_fingering
            for function in self.penalty_functions:
                distance += function(f1, f2)
        return distance

    def neighbors(self, node: _Node) -> Iterable[_Node]:
        return self.index[node.position + 1]

    def is_goal_reached(self, current: _Node, goal: _Node) -> bool:
        return current.position == goal.position
