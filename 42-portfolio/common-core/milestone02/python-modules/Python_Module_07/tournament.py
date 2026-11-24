from ex0 import FlameFactory, AquaFactory
from ex0._base import CreatureFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    InvalidBattleStrategyError,
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
)

Opponent = tuple[CreatureFactory, BattleStrategy]


def run_tournament(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    print()
    creatures = [
        (factory.create_base(), strategy)
        for factory, strategy in opponents
    ]

    try:
        for first_index, (first, first_strategy) in enumerate(creatures):
            for second, second_strategy in creatures[first_index + 1:]:
                print("* Battle *")
                print(first.describe())
                print(" vs.")
                print(second.describe())
                print(" now fight!")
                for action in first_strategy.act(first):
                    print(action)
                for action in second_strategy.act(second):
                    print(action)
                print()
    except InvalidBattleStrategyError as e:
        print(f"Battle error, aborting tournament: {e}")
        print()


def main() -> None:
    print("Tournament 0 (basic)")
    print("[ (Flameling+Norms), (Healing+Defensive) ]")

    run_tournament(
        [
            (FlameFactory(), NormalStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy()),
        ]
    )

    print("Tournament 1 (error)")
    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")

    run_tournament(
        [
            (FlameFactory(), AggressiveStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy()),
        ]
    )

    print("Tournament 2 (multiple)")
    print("[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")

    run_tournament(
        [
            (AquaFactory(), NormalStrategy()),
            (HealingCreatureFactory(), DefensiveStrategy()),
            (TransformCreatureFactory(), AggressiveStrategy()),
        ]
    )


if __name__ == "__main__":
    main()
