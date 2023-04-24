from typing import Iterable
from dataclasses import dataclass

from astar import AStar  # type: ignore

from .bisonoric import AnnotatedBisonoricFingering


def find_best_fingerings(all_fingerings: list[set[AnnotatedBisonoricFingering]]) \
        -> list[AnnotatedBisonoricFingering]:
    finder = FingerFinder(all_fingerings)
    return finder.find()


@dataclass(frozen=True)
class Node:
    position: int
    annotated_fingering: AnnotatedBisonoricFingering | None


class FingerFinder(AStar):
    def __init__(self, fingerings: list[set[AnnotatedBisonoricFingering]]):
        self.index: dict[int, set[Node]] = {
            i: {Node(i, f) for f in f_set}
            for i, f_set in enumerate(fingerings)
        }

    def find(self) -> list[AnnotatedBisonoricFingering]:
        start = Node(-1, None)
        max_index = max(self.index.keys())
        goal = list(self.index[max_index])[0]
        # is_goal_reached() only checks position,
        # so I think we can use any final node.
        # ... but then why is the goal parameter needed on astar(start, goal)?

        return [
            node.annotated_fingering for node in self.astar(start, goal)
            if node.annotated_fingering is not None
        ]

    def heuristic_cost_estimate(self, current: Node, goal: Node) -> float:
        return goal.position - current.position

    def distance_between(self, n1: Node, n2: Node) -> float:
        # TODO: Make the weightings here configurable.
        distance = abs(n1.position - n2.position)
        assert distance == 1  # Should only be used with immediate neighbors
        if n1.annotated_fingering is not None and n2.annotated_fingering is not None:
            f1 = n1.annotated_fingering.fingering
            f2 = n2.annotated_fingering.fingering
            if f1.direction != f2.direction:
                # Maybe the cost of bellows change should depend on note length?
                distance += 1
            # TODO: Penalize finger shifts
            # TODO: Penalize outer columns
            # TODO: Penalize top row?
            # TODO: Penalize pull at the start of a measure?
        return distance

    def neighbors(self, node: Node) -> Iterable[Node]:
        return self.index[node.position + 1]

    def is_goal_reached(self, current: Node, goal: Node) -> bool:
        return current.position == goal.position
