import fileinput
from collections import Counter
from itertools import combinations


def parse():
    return [line.strip() for line in fileinput.input()]


def checksum(words):
    twice = 0
    thrice = 0

    for words in words:
        counter = Counter(words)
        times = set(counter.values())
        if 2 in times:
            twice += 1
        if 3 in times:
            thrice += 1
    return twice * thrice


def search(words):
    for a, b in combinations(words, 2):
        equals = []
        diffs = 0
        for la, lb in zip(a, b):
            if la != lb:
                diffs += 1
            else:
                equals.append(la)

            if diffs > 1:
                break

        if diffs == 1:
            return "".join(equals)


def main():
    words = parse()
    print(f"Part 1: {checksum(words)}")
    common = search(words)
    print(f"Part 2: {common}")


if __name__ == "__main__":
    main()
