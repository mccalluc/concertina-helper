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
    pass

class BisonoricLayout(Layout):
    def init(self, push_layout, pull_layout):
        self.push_layout = push_layout
        self.pull_layout = pull_layout
    def get_fingerings(self, pitch: Pitch):
        return self.push_layout.get_fingerings(pitch) | self.pull_layout.get_fingerings()

class CGAngloPushLayout(UnisonoricLayout):
    pass

class CGAngloPullLayout(UnisonoricLayout):
    pass

class CGAngloLayout(BisonoricLayout):
    