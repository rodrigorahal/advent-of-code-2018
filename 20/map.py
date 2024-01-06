import fileinput
from collections import deque

DIRS = {
    "N": (-1, 0),
    "S": (1, 0),
    "W": (0, -1),
    "E": (0, 1),
}


def parse():
    pattern = fileinput.input().readline().strip()
    return pattern


def walk(pattern):
    grid = dict()
    i = 0
    row, col = 0, 0
    grid[row, col] = "X"
    pos = [(row, col)]

    while i < len(pattern):
        char = pattern[i]

        if char == "(":
            npos = []
            for row, col in pos:
                stops, j = walk_group(grid, row, col, pattern, i + 1)
                npos.extend(stops)
            i = j
            pos = npos

        elif char in "^$":
            i += 1

        else:
            npos = []
            for row, col in pos:
                nrow, ncol = mark(grid, row, col, char)
                npos.append((nrow, ncol))
            pos = npos
            i += 1
    return grid


def walk_group(grid, row, col, pattern, i):
    stops = []
    srow, scol = row, col

    while i < len(pattern):
        char = pattern[i]

        if char == ")":
            stops.append((row, col))
            return stops, i + 1

        elif char == "(":
            nested_stops, j = walk_group(grid, row, col, pattern, i + 1)
            stops.extend(nested_stops)
            i = j

        elif char == "|":
            stops.append((row, col))
            row, col = srow, scol
            i += 1

        else:
            row, col = mark(grid, row, col, char)
            i += 1
    return stops, i


def mark(grid, row, col, dir):
    dr, dc = DIRS[dir]
    nrow, ncol = row + dr, col + dc
    grid[nrow, ncol] = "-" if dr else "|"
    row, col = nrow, ncol
    nrow, ncol = row + dr, col + dc
    grid[nrow, ncol] = "."
    row, col = nrow, ncol
    return row, col


def display(grid):
    rows = [row for (row, col) in grid]
    cols = [col for (row, col) in grid]

    minrow, maxrow = min(rows), max(rows)
    mincol, maxcol = min(cols), max(cols)

    for row in range(minrow - 1, maxrow + 2):
        line = []
        for col in range(mincol - 1, maxcol + 2):
            line.append(grid.get((row, col), "#"))
        print("".join(line))
    print()


def search(grid, row, col):
    seen = set()
    queue = deque([(row, col, 0)])
    paths = dict()

    while queue:
        row, col, steps = queue.popleft()

        if (row, col) in seen:
            continue

        seen.add((row, col))
        paths[row, col] = steps

        for dr, dc in DIRS.values():
            if (row + dr, col + dc) in grid:
                if (dr and grid[row + dr, col + dc] == "-") or (
                    dc and grid[row + dr, col + dc] == "|"
                ):
                    queue.append((row + (2 * dr), col + (2 * dc), steps + 1))
    return paths


def main():
    pattern = parse()
    grid = walk(pattern)
    paths = search(grid, 0, 0)
    print(f"Part 1: {max(paths.values())}")
    print(f"Part 2: {sum(1 for v in paths.values() if v >= 1_000)}")


if __name__ == "__main__":
    main()
