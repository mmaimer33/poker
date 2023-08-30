# Poker Competition
---

Welcome to the Poker Competition! This project is a simulation of a poker game where bots compete against each other. The goal of this project is to create the bot that has more wins in a set of 10<sup>[`1`](#footnotes)</sup> games conducted between both bots.

## Rules

- The game will follow the standard Texas Hold'em rules. You can read more about the rules [here](https://en.wikipedia.org/wiki/Texas_hold_%27em).
- Each bot will start with a fixed amount of chips.
- The game will continue until only one bot has chips remaining or until a set number of rounds have been played. Tentatively, this number has been set to 20.
- The winner will be the player with the most chips at the end of the game.

## Requirements

- Python 3.x
- You must write a `Player` subclass with the required functionality.
- Your player subclass must have the name `Player-GITHUB`, where `GITHUB` is your GitHub username.

### Allowed libraries

- `random`
- `math`
- `numpy`
- `pandas`
- `enum`

Others can be discussed.

## Getting Started

1. Fork the repository.
2. Clone your fork.
3. Start writing `player.py`.

## Provided Files
- `player.py` has a template for the `Player` class that you will need to extend.
- `game.py` is the main file that will run the game.

Good luck and have fun!

## Footnotes
[`1`]: This number is subject to change.