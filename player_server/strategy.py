from models import Answer
from .interfaces import GuessStrategy, PlayerInterface

class BinarySearch(GuessStrategy):

    def next_guess(self, player: PlayerInterface) -> int:
        if not player.history:
            player._lower_bound = player.MIN
            player._upper_bound = player.MAX

        else:
            prev_guess, prev_answer = player.history[-1]
            # update search window
            if prev_answer == Answer.HIGHER:
                player._lower_bound = prev_guess
            elif prev_answer == Answer.LOWER:
                player._upper_bound = prev_guess

        # pick next guess
        next_pivot = int(player._lower_bound + (player._upper_bound - player._lower_bound) / 2)
        return next_pivot
  