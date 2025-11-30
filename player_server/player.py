from dataclasses import dataclass

from models import Answer
from .interfaces import GuessStrategy, MasterClientInterface

@dataclass
class Player():
    """the player is the core agent of the player server.

    It uses a GuessStrategy to determine the next guess and a MasterClientInterface to talk to the game master server.
    """
    strategy        : GuessStrategy
    master_client   : MasterClientInterface
    player_id       : str
    history         : list[tuple[int, Answer]]
    game_min        : int
    game_max        : int
    lower_bound     : int
    upper_bound     : int

    def __init__(self, strategy: GuessStrategy,
                 master_client: MasterClientInterface):
        self.strategy = strategy
        self.master_client = master_client
        self.history = []

    def get_lower_bound(self) -> int:
        """extract the highest guess which returned 'lower'
        """
        return self.lower_bound

    def get_upper_bound(self) -> int:
        """extract the lowest guess which returned 'higher'
        """
        return self.upper_bound

    def get_id(self) -> str:
        # return self.headers.get("player-id")
        if self.player_id is None:
            raise Exception("Player ID is not set. This could mean the game was not initialised.")
        return self.player_id
    
    def set_id(self, player_id: str | dict) -> None:
        if isinstance(player_id, dict):
            self.player_id = player_id.get("player-id") # type: ignore
        else:
            self.player_id = player_id

    def add_guess(self, guess: int, answer: Answer) -> None:
        """add a guess and its answer to the player's history and update bounds"""
        self.history.append((guess, answer))
        if self.strategy:
            if answer == Answer.LOWER and guess < self.upper_bound:
                self.upper_bound = guess
            elif answer == Answer.HIGHER and guess > self.lower_bound:
                self.lower_bound = guess
        return

    def get_last_answer(self) -> Answer | None:
        if self.history:
            return self.history[-1][1]
        return None

    def summarize_history(self) -> dict:
        status = Answer.WON if self.get_last_answer() == Answer.WON else "playing"
        n_guesses = len(self.history)
        number = self.history[-1][0] if self.history[-1][1] == Answer.WON else "unknown"

        return {"status": status,
                "number": number,
                "number of guesses": n_guesses,
                "history": self.history}

    def init_game(self, game_min:int, game_max:int) -> None:
        """Start the game and set the assigned playerID
        """
        headers = self.master_client.init_game(game_min, game_max)
        self.set_id(headers)
        self.game_min = game_min
        self.game_max = game_max
        self.lower_bound = game_min
        self.upper_bound = game_max
        return

    def take_guess(self, guess: int) -> Answer:
        """send a guess to the game master

        Args:
            guess (int): the guessed number

        Returns:
            str|dict: the game masters response to the guess
        """
        return self.master_client.guess(guess, self.get_id())
        
    def play_game(self):
        """play the number guessing game.

        based on players strategy, pick a guess, take the guess and safe the Answer.
        """
        while self.get_last_answer() != Answer.WON or not self.history:
            next_guess = self.strategy.next_guess(player=self)
            ans = self.take_guess(next_guess)
            self.add_guess(next_guess, ans)

