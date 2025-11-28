# Number guessing service

This is a small coding project. Posed by itdesign GmbH and implemented by Niclas Grote.

## Task

Implement two Python servers, that play the number-guessing game. The Master thinks of a configurable number from 1 to 1000 and the player tries to guess it. They communicate via HTTP requests. We can talk with the player, tell them to start a new round and watch them play.

## Execution Intructions

This project holds two containerized python servers. The game master (master-server) and the player (player-server).  
You can either run the containers together using `docker compose` or manually using `docker run`.

> [!IMPORTANT]
> Docker needs root privileges. Either run docker commands as root or as a user, who is part of the privilledged `docker` group.

### Run via docker compose

from the project root, run:

```shell
sudo docker compose up
```

to stop the containers, run:

```shell
sudo docker compose down
```

### Run manually

from the project root:

1. build the images  
```shell
sudo docker build -t master-server -f master_server/Dockerfile
sudo docker build -t player-server -f player_server/Dockerfile
```
2. run the containers
```shell
sudo docker run master-server
sudo docker run player-server
```
3. verify
```shell
# you can play a game by sending a request to the player server
curl -f http://localhost:8001/play
```

### a few remarks

- the master server listens on port 8000 (both externally and inside the container)
- the player server listens on port 8001 (both externally and inside the container)
- run `pytest .` in the project root to run the integration tests
- when using docker-compose, check the containers health status via:  

```shell
sudo docker containers ls
```

- if docker is not permittet on your system (often due its demand in privileges), you can use `podman` instead, which works like a rootless docker alias. Hence, you can even `podman compose up`.
