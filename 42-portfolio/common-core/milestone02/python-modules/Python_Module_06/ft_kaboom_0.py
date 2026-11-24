import alchemy.grimoire


def main() -> None:
    print("=== Kaboom 0 ===")
    print("Using grimoire module directly")

    spell_record = alchemy.grimoire.light_spell_record(
        'Fantasy',
        'Earth, wind and fire'
    )
    print(f"Testing record light spell: {spell_record}")


if __name__ == "__main__":
    main()
