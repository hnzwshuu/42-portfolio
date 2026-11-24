from collections.abc import Callable


Spell = Callable[[str, int], str]
Condition = Callable[[str, int], bool]


def spell_combiner(
    spell1: Spell,
    spell2: Spell,
) -> Callable[[str, int], tuple[str, str]]:
    def combined_spell(target: str, power: int) -> tuple[str, str]:
        return spell1(target, power), spell2(target, power)

    return combined_spell


def power_amplifier(base_spell: Spell, multiplier: int) -> Spell:
    def amplified_spell(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified_spell


def conditional_caster(condition: Condition, spell: Spell) -> Spell:
    def conditional_spell(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return conditional_spell


def spell_sequence(spells: list[Spell]) -> Callable[[str, int], list[str]]:
    def sequenced_spell(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]

    return sequenced_spell


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target} with {power} power"


def heal(target: str, power: int) -> str:
    return f"Heal restores {target} for {power} HP"


if __name__ == "__main__":
    print()
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined('Dragon', 20)
    print(f"Combined spell result: {result[0]}, {result[1]}")

    print()
    print("Testing power amplifier...")
    mega_fireball = power_amplifier(fireball, 3)
    print(f"Original: {fireball('Dragon', 10)}")
    print(f"Amplified: {mega_fireball('Dragon', 10)}")

    print()
    print("Testing conditional caster...")
    safe_fireball = conditional_caster(
        lambda target, power: power >= 15,
        fireball,
    )
    print(safe_fireball("Dragon", 10))
    print(safe_fireball("Dragon", 15))

    print()
    print("Testing spell sequence...")
    print(f"fireball is callable: {callable(fireball)}")
    print(f"heal is callable: {callable(heal)}")
    sequence = spell_sequence([fireball, heal])
    print(sequence("Dragon", 25))
