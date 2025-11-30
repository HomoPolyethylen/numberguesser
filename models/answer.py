"""this module contains the Answer enum used by both master and player"""

from enum import Enum

class Answer(Enum):
    """Answers, the game master can send to a guess.
    this class is used by both master and player.
    """
    HIGHER  = "higher"
    LOWER   = "lower"
    WON     = "won"

    def __eq__(self, other):
        """compare equality string-based"""
        return self.value == str(other)

    def __str__(self):
        """string representation of the Answer"""
        return self.value
