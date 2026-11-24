#! /usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float, age: int) -> None:
        self.name = name
        self._height = 0.0
        self._age = 0
        self.set_height(height, is_print=False)
        self.set_age(age, is_print=False)

    def set_height(self, height: float, is_print: bool = True) -> bool:
        if height < 0:
            print(f"{self.name}: Error, height can't be negative")
            return False
        else:
            self._height = height
            if is_print:
                print(f"Height updated: {self._height:g}cm")
            return True

    def set_age(self, age: int, is_print: bool = True) -> bool:
        if age < 0:
            print(f"{self.name}: Error, age can't be negative")
            return False
        else:
            self._age = age
            if is_print:
                print(f"Age updated: {self._age} days")
            return True

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    def show(self) -> None:
        print(f"{self.name}: {self._height:.1f}cm, {self._age} days old")


def main() -> None:
    rose = Plant("Rose", 15.0, 10)
    print("=== Garden Security System ===")
    print("Plant created: ",  end="")
    rose.show()
    print()
    rose.set_height(25)
    rose.set_age(30)
    print()
    if not rose.set_height(-1):
        print("Height update rejected")
    if not rose.set_age(-1):
        print("Age update rejected")
    print()
    print("Current state: ", end="")
    rose.show()


if __name__ == "__main__":
    main()
