import fileinput
from copy import deepcopy


def run(grid, steps):
    current = grid
    for s in range(1, steps):
        current = step(current)
        if s % 10 == 0:
            print(s)
            print(resource(current))
    return current


def detect_cycle(grid, steps):
    seen = {}
    resource_by_step = {}
    current = grid
    for s in range(1, steps):
        current = step(current)
        res = resource(current)
        if res in seen:
            # print(res, s, seen[res])
            pass
        else:
            seen[res] = s
            resource_by_step[s] = res
            s += 1
    return resource_by_step


def resource(grid):
    trees = lumberyards = 0
    for row, state in enumerate(grid):
        for col, acre in enumerate(state):
            if acre == "|":
                trees += 1
            elif acre == "#":
                lumberyards += 1
    return trees * lumberyards


def step(grid):
    updated = deepcopy(grid)

    for row, state in enumerate(grid):
        for col, acre in enumerate(state):
            adjacent = get_adjacent(grid, row, col)
            trees = sum(grid[nr][nc] == "|" for (nr, nc) in adjacent)
            lumberyards = sum(grid[nr][nc] == "#" for (nr, nc) in adjacent)

            if acre == ".":
                if trees >= 3:
                    updated[row][col] = "|"
            elif acre == "|":
                if lumberyards >= 3:
                    updated[row][col] = "#"
            elif acre == "#":
                if not (lumberyards >= 1 and trees >= 1):
                    updated[row][col] = "."
    return updated


def get_adjacent(grid, row, col):
    H, W = len(grid), len(grid[0])
    res = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dc == 0 and dr == 0:
                continue
            if 0 <= row + dr < H and 0 <= col + dc < W:
                res.append((row + dr, col + dc))
    return res


def parse():
    grid = []
    for line in fileinput.input():
        grid.append([char for char in line.strip()])
    return grid


def draw(grid):
    for row in grid:
        print("".join(row))


def main():
    grid = parse()
    updated = run(grid, steps=11)
    print(f"Part 1: {resource(updated)}")

    resource_by_step = detect_cycle(grid, steps=1_000)
    # cycle starts at step 481, with first repeated value at step 453
    start, first_seen = 481, 453
    # cycle repeats after every 28 steps
    cycle_every = 28
    # resource in the cycle is
    idx = (1_000_000_000 - start) % cycle_every
    print(f"Part 2: {resource_by_step[first_seen+idx]}")


if __name__ == "__main__":
    main()
