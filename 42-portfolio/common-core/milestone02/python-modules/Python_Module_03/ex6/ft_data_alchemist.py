#!/usr/bin/env python3

import random


def main() -> None:
    print("=== Game Data Alchemist ===")
    print()
    players = [
        "Alice",
        "bob",
        "Charlie",
        "dylan",
        "Emma",
        "Gregory",
        "john",
        "kevin",
        "Liam",
    ]
    print(f"Initial list of players: {players}")
    capitalized_players = [name.capitalize() for name in players]
    print(f"New list with all names capitalized: {capitalized_players}")
    only_capitalized = [name for name in players if name == name.capitalize()]
    print(f"New list of capitalized names only: {only_capitalized}")
    print()
    scores = {name: random.randint(1, 1000) for name in capitalized_players}
    print(f"Score dict: {scores}")
    average = sum(scores[name] for name in capitalized_players) / len(scores)
    print(f"Score average is {round(average, 2)}")
    high_scores = {
        name: scores[name]
        for name in scores
        if scores[name] > average
    }
    print(f"High scores: {high_scores}")


if __name__ == "__main__":
    main()
