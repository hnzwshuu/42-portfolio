#!/usr/bin/env python3

import random

ACHIEVEMENTS = [
    "First Steps",
    "Boss Slayer",
    "Treasure Hunter",
    "Master Explorer",
    "Speed Runner",
    "Untouchable",
    "World Savior",
    "Creating Genius",
    "Strategist",
    "Collector Supreme",
    "Survivor",
    "Unstoppable",
    "Sharp Mind",
    "Hidden Path Finder",
]


def gen_player_achievements() -> set[str]:
    achievement_count = random.randint(7, 10)
    return set(random.sample(ACHIEVEMENTS, achievement_count))


def get_all_distinct(alice: set[str], bob: set[str],
                     charlie: set[str], dylan: set[str]) -> set[str]:
    return alice.union(bob).union(charlie).union(dylan)


def get_common_achievements(alice: set[str], bob: set[str],
                            charlie: set[str], dylan: set[str]) -> set[str]:
    return alice.intersection(bob).intersection(charlie).intersection(dylan)


def get_unique_achievements(player: set[str],
                            first_other: set[str],
                            second_other: set[str],
                            third_other: set[str]) -> set[str]:
    other_achievements = first_other.union(second_other).union(third_other)
    return player.difference(other_achievements)


def get_missing_achievements(player: set[str]) -> set[str]:
    return set(ACHIEVEMENTS).difference(player)


def main() -> None:
    print("=== Achievement Tracker System ===")
    print()
    alice = gen_player_achievements()
    bob = gen_player_achievements()
    charlie = gen_player_achievements()
    dylan = gen_player_achievements()
    print(f"Player Alice: {alice}")
    print(f"Player Bob: {bob}")
    print(f"Player Charlie: {charlie}")
    print(f"Player Dylan: {dylan}")
    print()
    print(f"All distinct achievement: \
{get_all_distinct(alice, bob, charlie, dylan)}")
    print()
    print(f"Common achievement: \
{get_common_achievements(alice, bob, charlie, dylan)}")
    print()
    print(f"Only Alice has: \
{get_unique_achievements(alice, bob, charlie, dylan)}")
    print(f"Only Bob has: \
{get_unique_achievements(bob, alice, charlie, dylan)}")
    print(f"Only Charlie has: \
{get_unique_achievements(charlie, alice, bob, dylan)}")
    print(f"Only Dylan has: \
{get_unique_achievements(dylan, alice, bob, charlie)}")
    print()
    print(f"Alice is missing: \
{get_missing_achievements(alice)}")
    print(f"Bob is missing: {get_missing_achievements(bob)}")
    print(f"Charlie is missing: {get_missing_achievements(charlie)}")
    print(f"Dylan is missing: {get_missing_achievements(dylan)}")


if __name__ == "__main__":
    main()
