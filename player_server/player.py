from dataclasses import dataclass

from models import Answer
from .interfaces import GuessStrategy, MasterClientInterface, PlayerInterface

@dataclass
class Player(PlayerInterface):
    """the player is the core agent of the player server.

    It uses a GuessStrategy to determine the next guess and a MasterClientInterface to talk to the game master server.
    """
    strategy        : GuessStrategy
    master_client   : MasterClientInterface
    headers          : dict  = None
    MIN, MAX                = None, None
    history                 = []

    _lower_bound    : int   = MIN
    _upper_bound    : int   = MAX

    def get_lower_bound(self) -> int:
        """extract the highest guess which returned 'lower'
        """
        return self._lower_bound
        # elif self.history:
            # return min([guess[0] for guess in self.history if guess[1] == Answer.LOWER])

    def get_upper_bound(self) -> int:
        """extract the lowest guess which returned 'higher'
        """
        return self._upper_bound
        # if self.history:
            # return max([guess[0] for guess in self.history if guess[1] == Answer.HIGHER])

    def get_player_id(self) -> str:
        return self.headers.get("player-id")
    
    def set_player_id(self, id: str) -> None:
        if self.headers is None:
            self.headers = {}
        self.headers["player-id"] = id

    def add_guess(self, guess: int, answer: Answer) -> None:
        self.history.append((guess, answer))
        if self.strategy:
            if answer == Answer.LOWER and guess < self._upper_bound:
                self._upper_bound = guess
            elif answer == Answer.HIGHER and guess > self._lower_bound:
                self._lower_bound = guess
        return

    def get_last_answer(self) -> Answer:
        if self.history:
            return self.history[-1][1]
        else:
            return None

    def summarize_history(self) -> dict:
        status = Answer.WON if self.get_last_answer() == Answer.WON else "playing"
        n_guesses = len(self.history)

        return {"status": status,
                "number of guesses": n_guesses,
                "history": self.history}

    def init_game(self, game_min:int=MIN, game_max:int=MAX) -> None:
        """Start the game and set the assigned playerID
        """
        id = self.master_client.init_game(game_min, game_max)
        self.set_player_id(id)
        self.MIN = game_min
        self.MAX = game_max
        return

    def take_guess(self, guess: int) -> Answer:
        """send a guess to the game master

        Args:
            guess (int): the guessed number

        Returns:
            str|dict: the game masters response to the guess
        """
        return self.master_client.guess(guess)
        
    def play_game(self):
        """play the number guessing game.

        based on players strategy, pick a guess, take the guess and safe the Answer.
        """
        while self.get_last_answer() != Answer.WON or not self.history:
            next_guess = self.strategy.next_guess(player=self)
            ans = self.take_guess(next_guess)
            self.add_guess(next_guess, ans)

