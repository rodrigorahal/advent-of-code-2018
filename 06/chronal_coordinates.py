import fileinput
from collections import defaultdict


def parse():
    return [tuple(map(int, line.strip().split(", "))) for line in fileinput.input()]


def areas(coordinates):
    internals = internal(coordinates)
    (minx, maxx), (miny, maxy) = dimensions(coordinates)
    area_by_coordinate = defaultdict(int)

    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            base = closest((x, y), coordinates)
            if base and base in internals:
                area_by_coordinate[base] += 1

    return area_by_coordinate


def internal(coordinates):
    internals = set()
    for (x, y) in coordinates:
        left = right = top = bottom = None
        for (nx, ny) in coordinates:
            if (x, y) != (nx, ny):
                if x > nx:
                    left = (nx, ny)
                elif x < nx:
                    right = (nx, ny)
                if y > ny:
                    top = (nx, ny)
                elif y < ny:
                    bottom = (nx, ny)
        if all((left, right, top, bottom)):
            internals.add((x, y))
    return internals


def dimensions(coordinates):
    xs = [x for x, _ in coordinates]
    ys = [y for _, y in coordinates]
    return (min(xs), max(xs)), (min(ys), max(ys))


def distance(a, b):
    x, y = a
    nx, ny = b
    return abs(nx - x) + abs(ny - y)


def closest(p, coordinates):
    dists = sorted([(distance(p, a), a) for a in coordinates])

    return dists[0][1] if dists[0][0] != dists[1][0] else None


def largest(coordinates, limit):
    (minx, maxx), (miny, maxy) = dimensions(coordinates)

    region = set()

    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            total = sum([distance((x, y), a) for a in coordinates])
            if total < limit:
                region.add((x, y))

    return len(region)


def main():
    coordinates = parse()
    area_by_coordinate = areas(coordinates)

    area = max(area_by_coordinate.values())
    print(f"Part 1: {area}")

    LIMIT = 10_000
    region = largest(coordinates, LIMIT)
    print(f"Part 2: {region}")


if __name__ == "__main__":
    main()
