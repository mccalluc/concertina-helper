from typing import Iterable
from dataclasses import dataclass

from astar import AStar  # type: ignore

from .layouts.bisonoric import AnnotatedBisonoricFingering
from .penalties import PenaltyFunction


def find_best_fingerings(
    all_fingerings: Iterable[set[AnnotatedBisonoricFingering]],
    penalty_functions: Iterable[PenaltyFunction]
) -> Iterable[AnnotatedBisonoricFingering]:
    '''
    Given a list of sets of possible fingerings,
    returns a list representing the best fingerings.
    See `concertina_helper.notes_on_layout.NotesOnLayout.get_best_fingerings`
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
            fingerings: Iterable[set[AnnotatedBisonoricFingering]],
            penalty_functions: Iterable[PenaltyFunction]):
        self.penalty_functions = penalty_functions
        self.index: dict[int, set[_Node]] = {
            i: {_Node(i, f) for f in f_set}
            for i, f_set in enumerate(fingerings)
        }

    def find(self) -> Iterable[AnnotatedBisonoricFingering]:
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
