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
    annotated_fingering: AnnotatedBisonoricFingering


class FingerFinder(AStar):
    def __init__(self, fingerings: list[set[AnnotatedBisonoricFingering]]):
        self.index = {
            i: frozenset(Node(i, f) for f in f_set)
            for i, f_set in enumerate(fingerings)
        }

    def find(self):
        start = list(self.index[0])[0]
        max_index = max(self.index.keys())
        goal = list(self.index[max_index])[0]
        return [node.annotated_fingering for node in self.astar(start, goal)]

    def heuristic_cost_estimate(self, current: Node, goal: Node) -> float:
        return goal.position - current.position

    def distance_between(self, n1: Node, n2: Node) -> float:
        # TODO: Make the weightings here configurable.
        distance = abs(n1.position - n2.position)
        f1 = n1.annotated_fingering.fingering
        f2 = n2.annotated_fingering.fingering
        if f1.direction != f2.direction:
            # Maybe the cost of bellows change should depend on note length?
            distance += 1
        # TODO: Penalize finger shifts
        # TODO: Penalize outer columns
        # TODO: Penalize top row?
        return distance

    def neighbors(self, node) -> Iterable[Node]:
        return self.index[node.position + 1]

    def is_goal_reached(self, current: Node, goal: Node) -> bool:
        # There could be multiple fingerings for the last note.
        # They are all equally good.
        return current.position == goal.position
