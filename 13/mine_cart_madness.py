import fileinput
from copy import deepcopy
from itertools import cycle

TURNS = {
    (">", "\\"): "v",
    (">", "/"): "^",
    ("<", "\\"): "^",
    ("<", "/"): "v",
    ("^", "\\"): "<",
    ("^", "/"): ">",
    ("v", "\\"): ">",
    ("v", "/"): "<",
}

INTERSECTIONS = {
    (">", "L"): "^",
    (">", "R"): "v",
    (">", "S"): ">",
    ("<", "L"): "v",
    ("<", "R"): "^",
    ("<", "S"): "<",
    ("^", "L"): "<",
    ("^", "R"): ">",
    ("^", "S"): "^",
    ("v", "L"): ">",
    ("v", "R"): "<",
    ("v", "S"): "v",
}


def parse():
    grid = dict()
    carts = dict()
    for r, line in enumerate(fileinput.input()):
        for c, item in enumerate(line):
            if item in ("^", "v", ">", "<"):
                carts[(r, c)] = (item, cycle(["L", "S", "R"]))

                if item in ("^", "v"):
                    grid[(r, c)] = "|"
                elif item in (">", "<"):
                    grid[(r, c)] = "-"

            elif item in ("|", "-", "/", "\\", "+"):
                grid[(r, c)] = item
    return grid, carts


def run(grid, carts, until_last=False):
    carts = deepcopy(carts)
    while True:
        if until_last and len(carts) == 1:
            return next(iter(carts.keys()))

        carts, collision = tick(grid, carts, until_last)

        if collision and not until_last:
            return collision


def tick(grid, carts, until_last=False):
    updated_carts = {k: v for k, v in carts.items()}
    crashed = set()

    for r, c in sorted(carts):
        if (r, c) in crashed:
            continue

        cart, intersection = carts[(r, c)]

        row = r
        col = c

        if cart == "^":
            row -= 1
        elif cart == "v":
            row += 1
        elif cart == ">":
            col += 1
        elif cart == "<":
            col -= 1

        del updated_carts[(r, c)]

        if (row, col) in updated_carts:
            # collision
            if until_last:
                crashed.add((row, col))
                del updated_carts[(row, col)]
                continue
            else:
                return updated_carts, (row, col)

        track = grid[(row, col)]

        if track not in ("/", "\\", "+"):
            updated_cart = cart
        elif track in ("/", "\\"):
            updated_cart = TURNS[((cart, track))]
        elif track == "+":
            updated_cart = INTERSECTIONS[(cart, next(intersection))]

        updated_carts[(row, col)] = (updated_cart, intersection)

    return updated_carts, None


def display(grid, carts):
    def value(r, c):
        if (r, c) in carts:
            return carts[(r, c)][0]
        return grid.get((r, c), " ")

    rs = [r for r, c in grid]
    cs = [c for r, c in grid]

    minr, maxr = min(rs), max(rs)
    minc, maxc = min(cs), max(cs)

    for r in range(minr, maxr + 1):
        print("".join(value(r, c) for c in range(minc, maxc + 1)))


def main():
    grid, carts = parse()
    row, col = run(grid, carts)
    print(f"Part 1: {col,row}")
    row, col = run(grid, carts, until_last=True)
    print(f"Part 2: {col,row}")


if __name__ == "__main__":
    main()
