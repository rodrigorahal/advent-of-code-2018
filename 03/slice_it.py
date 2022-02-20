import fileinput
from collections import Counter, defaultdict


def parse():
    claims = []

    for line in fileinput.input():
        words = line.strip().split(" ")
        id = words[0][1:]
        left, top = tuple(map(int, words[2].strip(":").split(",")))
        width, height = tuple(map(int, words[3].split("x")))

        claims.append((id, (left, top), (width, height)))
    return claims


def count(claims):
    counter = Counter()
    for _, (left, top), (width, height) in claims:
        for y in range(top, top + height):
            for x in range(left, left + width):
                counter[(x, y)] += 1
    return sum(1 for c in counter.values() if c >= 2)


def overlaps(claims):
    belongs = defaultdict(set)
    for id, (left, top), (width, height) in claims:
        for y in range(top, top + height):
            for x in range(left, left + width):
                belongs[(x, y)].add(id)

    overlapped = set()
    for point_claims in belongs.values():
        if len(point_claims) > 1:
            overlapped.update(point_claims)

    for id, _, _ in claims:
        if id not in overlapped:
            return id


def main():
    claims = parse()
    print(f"Part 1: {count(claims)}")
    print(f"Part 2: {overlaps(claims)}")


if __name__ == "__main__":
    main()
