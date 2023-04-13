from abc import ABC, abstractmethod
from enum import Enum, auto
from pyabc2 import Pitch

class Direction(Enum):
    PUSH = auto()
    PULL = auto()

class Fingering(ABC):
    pass

class UnisonoricFingering(Fingering):
    pass

class BisonoricFingering(Fingering):
    def __init__(self, direction: Direction, fingering: UnisonoricFingering):
        self.direction = direction
        self.fingering = fingering
    pass

class Layout(ABC):
    @abstractmethod
    def get_fingerings(pitch: Pitch) -> set(Fingering): pass


class UnisonoricLayout(Layout):
    def __init__(self, left: list[list[Pitch]], right: list[list[Pitch]]):
        self.left = left
        self.right = right

class BisonoricLayout(Layout):
    def __init__(self, push_layout: UnisonoricLayout = None, pull_layout: UnisonoricLayout = None):
        self.push_layout = push_layout
        self.pull_layout = pull_layout
    def get_fingerings(self, pitch: Pitch) -> set[BisonoricFingering]:
        push_fingerings = self.push_layout.get_fingerings(pitch)
        pull_fingerings = self.pull_layout.get_fingerings(pitch)
        return (
            {BisonoricFingering(Direction.PUSH, pf) for pf in push_fingerings} |
            {BisonoricFingering(Direction.PULL, pf) for pf in pull_fingerings}
        )

def names_to_pitches(matrix: list[list[str]]) -> list[list[Pitch]]:
    return [[Pitch.from_name(name) for name in row] for row in matrix]

cg_anglo_wheatstone_push_layout = UnisonoricLayout(
    names_to_pitches(
    [['E3', 'A3', 'C#4', 'A4', 'G#4'],
     ['C3', 'G3', 'C4', 'E4', 'G4'],
     ['B3', 'D4', 'G4', 'B4', 'D5']]),
    names_to_pitches(
    [['C#5', 'A5', 'G#5', 'C#6', 'A6'],
     ['C5', 'E5', 'G5', 'C6', 'E6'],
     ['G5', 'B5', 'D6', 'G6', 'B6']]),
)

cg_anglo_wheatstone_pull_layout = UnisonoricLayout(
    names_to_pitches(
    [['F3', 'Bb3', 'D#4', 'G4', 'Bb4'],
     ['G3', 'B3', 'D4', 'F4', 'A4'],
     ['A3', 'F#4', 'A4', 'C5', 'E5']]),
    names_to_pitches(
    [['D#5', 'G5', 'Bb5', 'D#6', 'F6'],
     ['B5', 'D5', 'F5', 'A5', 'B5'],
     ['F#5', 'A5', 'C6', 'E6', 'F#6']])
)

cg_anglo_wheatstone_layout = BisonoricLayout(
    push_layout=cg_anglo_wheatstone_push_layout,
    pull_layout=cg_anglo_wheatstone_pull_layout,
)
