from abc import ABC, abstractmethod

from ex0._base import Creature
from ex1._capabilities import HealCapability, TransformCapability


class InvalidBattleStrategyError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise InvalidBattleStrategyError(
                "Invalid Creature "
                f"'{creature._name}' for this aggressive strategy"
            )
        if not isinstance(creature, TransformCapability):
            raise InvalidBattleStrategyError(
                "Invalid aggressive strategy target"
            )
        return [creature.transform(), creature.attack(), creature.revert()]


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        if not self.is_valid(creature):
            raise InvalidBattleStrategyError(
                "Invalid Creature "
                f"'{creature._name}' for this defensive strategy"
            )
        if not isinstance(creature, HealCapability):
            raise InvalidBattleStrategyError(
                "Invalid defensive strategy target"
            )
        return [creature.attack(), creature.heal()]
