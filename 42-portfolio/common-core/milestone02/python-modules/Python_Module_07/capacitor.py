from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1._capabilities import HealCapability, TransformCapability


def test_healing_creatures() -> None:
    print("Testing Creature with healing capability")
    factory = HealingCreatureFactory()
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(" base:")
    print(base.describe())
    print(base.attack())
    if isinstance(base, HealCapability):
        print(base.heal())
    print(" evolved:")
    print(evolved.describe())
    print(evolved.attack())
    if isinstance(evolved, HealCapability):
        print(evolved.heal())


def test_transform_creatures() -> None:
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()
    for label, creature in (
        (" base:", factory.create_base()),
        (" evolved:", factory.create_evolved())
    ):
        print(label)
        print(creature.describe())
        print(creature.attack())
        if isinstance(creature, TransformCapability):
            print(creature.transform())
            print(creature.attack())
            print(creature.revert())


def main() -> None:
    test_healing_creatures()
    print()
    test_transform_creatures()


if __name__ == "__main__":
    main()
