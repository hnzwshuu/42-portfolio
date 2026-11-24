#!/usr/bin/env python3

import random
import typing

Event = tuple[str, str]


def gen_event() -> typing.Generator[Event, None, None]:
    players = ["bob", "alice", "dylan", "charlie"]
    actions = [
        "run",
        "eat",
        "sleep",
        "grab",
        "move",
        "climb",
        "swim",
        "release",
        "use",
    ]
    while True:
        yield (random.choice(players), random.choice(actions))


def consume_event(events: list[Event]) -> typing.Generator[Event, None, None]:
    while len(events) > 0:
        index = random.randrange(len(events))
        event = events[index]
        del events[index]
        yield event


def main() -> None:
    print("=== Game Data Stream Processor ===")
    event_stream = gen_event()
    for index in range(1000):
        name, action = next(event_stream)
        print(f"Event {index}: Player {name} did action {action}")
    events = [
        next(event_stream),
        next(event_stream),
        next(event_stream),
        next(event_stream),
        next(event_stream),
        next(event_stream),
        next(event_stream),
        next(event_stream),
        next(event_stream),
        next(event_stream),
    ]
    print(f"Build list of 10 events: {events}")
    for event in consume_event(events):
        print(f"Got event form list: {event}")
        print(f"Remain in list: {events}")


if __name__ == "__main__":
    main()
