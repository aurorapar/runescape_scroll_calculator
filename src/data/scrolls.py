from enum import Enum, auto

from .implings import Impling

class Scroll(Enum):
    BEGINNER = auto()
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()
    ELITE = auto()

SCROLL_PROBABILITIES = {}
for impling in Impling:
    SCROLL_PROBABILITIES[impling] = {
        Scroll: 0
    }

SCROLL_PROBABILITIES[Impling.BABY] = {
    Scroll.EASY: 1/50,
}

SCROLL_PROBABILITIES[Impling.YOUNG] = {
    Scroll.EASY: 1/50,
}

SCROLL_PROBABILITIES[Impling.GOURMET] = {
    Scroll.EASY: 1/50,
}

SCROLL_PROBABILITIES[Impling.EARTH] = {
    Scroll.MEDIUM: 1/30,
}

SCROLL_PROBABILITIES[Impling.ESSENCE] = {
    Scroll.MEDIUM: 1/30,
}

SCROLL_PROBABILITIES[Impling.ECLECTIC] = {
    Scroll.MEDIUM: 1/30,
}

SCROLL_PROBABILITIES[Impling.NATURE] = {
    Scroll.HARD: 1/15,
}

SCROLL_PROBABILITIES[Impling.MAGPIE] = {
    Scroll.HARD: 1/15,
}

SCROLL_PROBABILITIES[Impling.NINJA] = {
    Scroll.HARD: 1/15,
}
SCROLL_PROBABILITIES[Impling.DRAGON] = {
    Scroll.ELITE: 1/5,
}
