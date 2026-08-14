from __future__ import annotations
from dataclasses import dataclass
from typing import Literal


Handedness = Literal["Left", "Right"]


@dataclass(slots=True, frozen=True)
class Landmark:
    """
    A single hand landmark in normalised image coordinates.
    """

    x: float
    y: float
    z: float

    def distance_to(self, other : Landmark) -> float:

        dx = other.x - self.x
        dy = other.y - self.y
        distance = ((dx)**2 + (dy)**2) ** 0.5
        return distance

@dataclass(slots=True, frozen=True)
class Hand:
    """
    Detector-agnostic representation of a detected hand.
    """

    landmarks: list[Landmark]
    handedness: Handedness
    handedness_score: float

    @property
    def wrist(self) -> Landmark:
        return self.landmarks[0]

    @property
    def thumb_tip(self) -> Landmark:
        return self.landmarks[4]

    @property
    def index_tip(self) -> Landmark:
        return self.landmarks[8]

    @property
    def middle_tip(self) -> Landmark:
        return self.landmarks[12]

    @property
    def ring_tip(self) -> Landmark:
        return self.landmarks[16]

    @property
    def pinky_tip(self) -> Landmark:
        return self.landmarks[20]