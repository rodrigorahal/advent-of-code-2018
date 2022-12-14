import fileinput
import sys


def parse():
    coords = []
    for line in fileinput.input():
        a, b = line.strip().split(", ")

        if a.startswith("x"):
            x = int(a.strip("x="))
            y = tuple(map(int, b.strip("y=").split("..")))
            coords.append((x, x, *y))
        else:
            y = int(a.strip("y="))
            x = tuple(map(int, b.strip("x=").split("..")))
            coords.append((*x, y, y))

    grid = {}
    for x0, x1, y0, y1 in coords:
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                grid[(y, x)] = "#"

    grid[(0, 500)] = "+"

    return coords, grid


def edges(coords):
    xs = set()
    ys = set()
    for minx, maxx, miny, maxy in coords:
        xs.add(minx)
        xs.add(maxx)
        ys.add(miny)
        ys.add(maxy)

    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    return (minx, maxx), (miny, maxy)


def display(coords, grid):
    (minx, maxx), (miny, maxy) = edges(coords)
    for row in range(miny - 1, maxy + 2):
        print("".join([grid.get((row, col), ".") for col in range(minx - 1, maxx + 2)]))
    print()


def flow(grid, x, y, maxy, dir=0):
    if (y, x) not in grid:
        grid[(y, x)] = "|"

    if y == maxy:
        return

    if grid[(y, x)] == "#":
        return x

    if (y + 1, x) not in grid:
        flow(grid, x, y + 1, maxy)

    if grid[(y + 1, x)] in "~#":
        if dir:
            return flow(grid, x + dir, y, maxy, dir=dir)
        else:
            leftx = flow(grid, x - 1, y, maxy, dir=-1)
            rightx = flow(grid, x + 1, y, maxy, dir=1)
            if grid[(y, leftx)] == "#" and grid[(y, rightx)] == "#":
                for fillx in range(leftx + 1, rightx):
                    grid[(y, fillx)] = "~"
    else:
        return x


def main():
    coords, grid = parse()
    (minx, maxx), (miny, maxy) = edges(coords)

    flow(grid, 500, 0, maxy)
    # display(coords, grid)

    settled = sum(v == "~" for (y, x), v in grid.items() if miny <= y <= maxy)
    flowing = sum(v == "|" for (y, x), v in grid.items() if miny <= y <= maxy)
    print(f"Part 1: {settled + flowing}")
    print(f"Part 2: {settled}")


if __name__ == "__main__":
    sys.setrecursionlimit(3000)
    main()
