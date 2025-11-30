#!/usr/bin/env python3
"""This is the Player Server
It tries to guess the game master servers number using http requests
"""
import os
from fastapi import FastAPI, Depends

from .proxy import get_master_client
from .strategy import BinarySearch
from .interfaces import MasterClientInterface
from .player import Player

#
# GLOBs & CONSTs
#
app = FastAPI()
MIN = int(os.getenv("GAME_MIN", default="1"))
MAX = int(os.getenv("GAME_MAX", default="1000"))


#
# PATHS
#
@app.get("/health", status_code=200)
def get_health():
    """check if the server is healthy"""
    return "healthy"

@app.get("/ping-master", status_code=200)
def ping_master(client: MasterClientInterface = Depends(get_master_client)):
    """ping the master server to check connectivity"""
    r = client.get("/ping")
    return {"player received": r}

@app.get("/play", status_code=200)
def get_play(game_min: int = MIN,
             game_max: int = MAX,
             master_client: MasterClientInterface = Depends(get_master_client)):
    """play a game with the master server and return the result"""

    # initialize the game
    player = Player(BinarySearch(), master_client)
    player.init_game(game_min, game_max)

    # play the game
    player.play_game()

    # return result
    return player.summarize_history()
