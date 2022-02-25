from __future__ import annotations
from dataclasses import dataclass
from itertools import cycle


@dataclass
class Marble:
    id: int
    next: Marble = None
    prev: Marble = None


def play(players: int, last: int):
    scores = [0] * (players + 1)

    id = 0
    first = Marble(id=id)
    first.next = first
    first.prev = first
    curr = first

    for player in cycle(range(1, players + 1)):
        id += 1

        if id == last + 1:
            return max(scores)

        if id % 23 == 0:
            scores[player] += id

            for _ in range(7):
                to_remove = curr.prev
                curr = curr.prev

            curr = curr.next
            prev = to_remove.prev
            prev.next = curr
            curr.prev = prev

            scores[player] += to_remove.id

        else:
            marble = Marble(id=id)

            next = curr.next
            next_next = next.next
            marble.prev = next
            marble.next = next_next

            next.next = marble
            next_next.prev = marble

            curr = marble


def display(first: Marble):
    ids = [first.id]
    curr = first
    while curr.next.id != first.id:
        curr = curr.next
        ids.append(curr.id)
    print(ids)


def main():
    PLAYERS = 455
    LAST = 71223

    score = play(PLAYERS, LAST)
    print(f"Part 1: {score}")

    LAST *= 100
    score = play(PLAYERS, LAST)
    print(f"Part 2: {score}")


if __name__ == "__main__":
    main()
