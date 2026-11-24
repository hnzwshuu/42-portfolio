#!/usr/bin/env python3
import sys


def parse_inventory(args: list[str]) -> dict[str, int]:
    inventory: dict[str, int] = {}
    index = 1
    while index < len(args):
        parameter = args[index]
        parts = parameter.split(":")
        if len(parts) != 2 or parts[0] == "" or parts[1] == "":
            print(f"Error - invalid parameter '{parameter}'")
            index += 1
            continue
        item = parts[0]
        if item in inventory.keys():
            print(f"Redundant item '{item}' - discarding")
            index += 1
            continue
        try:
            inventory.update({item: int(parts[1])})
        except ValueError as e:
            print(f"Quantity error for '{item}': {e}")
        index += 1
    return inventory


def print_percentages(inventory: dict[str, int]) -> None:
    total_quantity = sum(inventory.values())
    for item in inventory.keys():
        print(f"Item {item} represents \
{round(inventory[item] * 100 / total_quantity, 1)}%")


def print_abundance(inventory: dict[str, int]) -> None:
    first_item = ""
    most_item = ""
    least_item = ""
    for item in inventory.keys():
        if first_item == "":
            first_item = item
            most_item = item
            least_item = item
        if inventory[most_item] < inventory[item]:
            most_item = item
        if inventory[least_item] > inventory[item]:
            least_item = item
    print(f"Item abundant: {most_item} with quantity {inventory[most_item]}")
    print(f"Item abundant: {least_item} with quantity {inventory[least_item]}")


def main() -> None:
    print("=== Inventory System Analysis ===")
    if len(sys.argv) <= 1:
        print("No scores provided. Usage: python3 ft_inventory_system.py \
<item_name1>:<quantity1> <item_name2>:<quantity2> ...")
        return
    inventory = parse_inventory(sys.argv)
    print(f"Got inventory: {inventory}")
    print(f"Item list: {list(inventory.keys())}")
    print(f"Total quantity of the \
{len(inventory)} items: {sum(inventory.values())}")
    if len(inventory) == 0 or sum(inventory.values()) == 0:
        print("Inventory is empty or has no quantity to analyze")
        inventory.update({"magic_item": 1})
        print(f"Updated inventory: {inventory}")
        return
    print_percentages(inventory)
    print_abundance(inventory)
    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
