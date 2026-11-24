#! /usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

    def grow(self) -> None:
        if self.name == "Rose":
            self.height += 0.8
        elif self.name == "Sunflower":
            self.height += 1.6
        elif self.name == "Cactus":
            self.height += 0.2
        else:
            self.height += 1.0

    def age_one_day(self) -> None:
        self.age += 1

    def show(self) -> None:
        print(f"{self.name}: {self.height:.1f}cm, {self.age} days old")


def main() -> None:
    plant = Plant("Rose", 25.0, 30)
    plant_first_height = plant.height

    print("=== Garden Plant Growth ===")
    plant.show()
    for i in range(1, 8):
        plant.grow()
        plant.age_one_day()
        print(f"=== Day {i} ===")
        plant.show()
    print(f"Growth this week: {(plant.height - plant_first_height):.1f}cm")


if __name__ == "__main__":
    main()
