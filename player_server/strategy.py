"""this module implements concrete guessing strategies for players to use"""

from models import Answer
from .interfaces import GuessStrategy
from .player import Player

class BinarySearch(GuessStrategy):
    """A guessing strategy that uses binary search to find the number in O(log n) time."""

    def next_guess(self, player: Player) -> int:
        if not player.history:
            player.lower_bound = player.game_min
            player.upper_bound = player.game_max

        else:
            prev_guess, prev_answer = player.history[-1]
            # update search window
            if prev_answer == Answer.HIGHER:
                player.lower_bound = prev_guess
            elif prev_answer == Answer.LOWER:
                player.upper_bound = prev_guess

        # pick next guess
        next_pivot = int(player.lower_bound + (player.upper_bound - player.lower_bound) / 2)
        return next_pivot
