#!/usr/bin/env python3
"""This is the Game Master Server

It can play number guessing with multiple player instances.
"""
from fastapi import FastAPI, HTTPException, Depends, Header
from typing import Annotated

from models import Answer
from .game import Game

#
# GLOBs
#
active_games = {}
app = FastAPI()

#
# DEPENDENCIES
#
def get_player_game(player_id: Annotated[str | None, Header()]) -> Game:
    """return a player's game, if it exists

    Args:
        player_id (str): the player id

    Raises:
        HTTPException: code 422: missing player-id in headers
        HTTPException: code 406: no active game for player found

    Returns:
        Game: the players active game
    """
    if player_id is None:
        raise HTTPException(status_code=422,
                            detail="missing player-id in headers")
    
    if player_id not in active_games:
        raise HTTPException(status_code=406,
                            detail=f"No Game active for specified player '{player_id}' found.\
                                Initialize a new game first.")
    
    return active_games[player_id]

#
# API REQUESTS
#
@app.get("/ping", status_code=200)
def get_ping():
    return "pong"

@app.get("/new-game", status_code=201)
def new_game(game_min: int = 1, game_max: int = 1000):
    """initialise a game instance and return a player id"""
    game = Game(game_min, game_max)
    active_games[game.player] = game
    return {"player-id": game.player}

@app.get("/games", status_code=200)
def get_games():
    return active_games

@app.get("/guess")
def handle_guess(guess: int, game: Annotated[Game, Depends(get_player_game)]) -> str:

    if guess < game.number:
        ans = Answer.HIGHER
    elif guess == game.number:
        ans = Answer.WON
    elif guess > game.number:
        ans = Answer.LOWER

    game.guesses.append((guess, ans))
    return str(ans)
