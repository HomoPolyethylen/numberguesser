# Number guessing service

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![Prettier](https://img.shields.io/badge/prettier-%23F7B93E.svg?style=for-the-badge&logo=prettier&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

This is a small coding project. Posed by itdesign GmbH and implemented by Niclas Grote.

## Task

Implement two Python servers, that play the number-guessing game. The Master thinks of a configurable number from 1 to 1000 and the player tries to guess it. They communicate via HTTP requests. We can talk with the player, tell them to start a new round and watch them play.

## Execution Intructions

This project holds two containerized python servers. The game master (master-server) and the player (player-server).  
You can either run the containers together using `docker compose` or manually using `docker run`.

> [!IMPORTANT]
> Docker needs root privileges. Either run docker commands as root or as a user, who is part of the privilledged `docker` group.
> If docker is not permitted on your system, use `podman` which, in most cases, can be used like a rootless docker alias.

### Run via docker compose

from the project root, run:

```shell
docker compose up
```

to stop the containers, run:

```shell
docker compose down
```

### Run manually

from the project root:

1. build the images

   ```shell
   docker build -t master-server -f master_server/Dockerfile
   docker build -t player-server -f player_server/Dockerfile
   ```

2. run the containers

   ```shell
   docker run master-server
   docker run player-server
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
  docker containers ls
  ```
