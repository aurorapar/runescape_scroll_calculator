from enum import Enum, auto

class Casket(Enum):
    BEGINNER = auto()
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()
    ELITE = auto()
    MASTER = auto()
    WATSON = auto()


WIKI_CASKET_REGEXES = {

    Casket.BEGINNER:    r'.*?On average, beginner clues are worth <span class=\"coins inventory-image \w+-\d+ coins-pos\">(\d+,*\d+\.*\d+)?(</span>)?.*',
    Casket.EASY:        r'.*?for a total expected value per clue of <span class=\"coins inventory-image \w+-\d+ coins-pos\">(\d+,*\d+\.*\d+)?</span>(</span>)?.*',
    Casket.MEDIUM:      r'.*?for a total expected value per clue of <span class=\"coins inventory-image \w+-\d+ coins-pos\">(\d+,*\d+\.*\d+)?</span>(</span>)?.*',
    Casket.HARD:        r'.*?for a total expected value per clue of <span class=\"coins inventory-image \w+-\d+ coins-pos\">(\d+,*\d+\.*\d+)?</span>(</span>)?.*',
    Casket.ELITE:       r'.*?for a total expected value per clue of <span class=\"coins inventory-image \w+-\d+ coins-pos\">(\d+,*\d+\.*\d+)?</span>(</span>)?.*',
    Casket.MASTER:      r'.*?for a total of <span class=\"coins inventory-image \w+-\d+ coins-pos\">(\d+,*\d+\.*\d+)?(</span>)?.*',
    Casket.WATSON:      r'.*?The expected value of the clues given to Watson is <span class=\"coins inventory-image \w+-\d+ coins-pos\">(\d+,*\d+\.*\d+)?(</span>)?.*',
}
