def ft_recursive(i: int, last_day: int) -> None:
    i += 1
    print(f"Day {i}")
    if i == last_day:
        return
    else:
        ft_recursive(i, last_day)
    return


def ft_count_harvest_recursive() -> None:
    last_day = int(input("Days until harvest: "))
    i = 0
    ft_recursive(i, last_day)
    print("Harvest time!")
