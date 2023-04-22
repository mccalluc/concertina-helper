from typing import Iterable
from itertools import chain
from dataclasses import dataclass

from astar import AStar  # type: ignore

from .layouts import BisonoricFingering


@dataclass(frozen=True)
class Node:
    position: int
    fingering: BisonoricFingering


class FingerFinder(AStar):
    def __init__(self, fingerings: list[set[BisonoricFingering]]):
        breakpoint()
        self.index = {
            i: frozenset(Node(i, f) for f in f_set)
            for i, f_set in enumerate(fingerings)
        }

    def heuristic_cost_estimate(self, current: Node, goal: Node) -> float:
        return goal.position - current.position

    def distance_between(self, n1: Node, n2: Node) -> float:
        # TODO: Make the weightings here configurable.
        distance = abs(n1.position - n2.position)
        f1 = n1.fingering
        f2 = n2.fingering
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

    # TODO: Add a wrapper for the astar() method that determines the start and end from self.index.
