#!/usr/bin/env python
"""test the player server endpoints.

depents on the test client fixtures defined in conftest.py
you might need to install the project in editable mode for pytest to find the modules:
`pip install -e . && pytest .`
"""

import httpx

def test_health(get_player_testing_client):
    """ping the health endpoint of the player server"""
    r = get_player_testing_client.get("/health")

    assert r.status_code == httpx.codes.OK
    assert r.json() == "healthy"


def test_ping_master(get_player_testing_client):
    """check if the player can talk to the master"""
    r = get_player_testing_client.get("/ping-master")

    assert r.status_code == httpx.codes.OK
    assert r.json() == {"player received": "pong"}

def test_play(get_player_testing_client):
    """test playing a complete game with the master server"""
    r = get_player_testing_client.get("/play", params={"game_min": 1, "game_max": 20})

    assert r.status_code == httpx.codes.OK
    assert "number of guesses" in r.json()
