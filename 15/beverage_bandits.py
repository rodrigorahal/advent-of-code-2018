from copy import deepcopy
import fileinput
from collections import deque
from operator import itemgetter


DAMAGE = {"G": 3, "E": 3}


def parse():
    grid = []
    G = {}
    E = {}
    for r, line in enumerate(fileinput.input()):
        row = []
        for c, char in enumerate(line.strip()):
            if char == "G":
                G[(r, c)] = 200
            elif char == "E":
                E[(r, c)] = 200
            row.append(char)
        grid.append(row)
    return grid, G, E


def display(grid):
    for row in grid:
        print("".join(char for char in row))
    print()


def play(grid, goblins, elfs, damage):
    rounds = 0
    while len(goblins) > 0 and len(elfs) > 0:
        finished = round(grid, goblins, elfs, damage)
        if finished:
            break
        rounds += 1

    return (
        rounds,
        goblins if len(goblins) > 0 else elfs,
        "G" if len(goblins) > 0 else "E",
    )


def display_points(goblins, elfs):
    print(f"G: {dict(sorted(goblins.items()))}")
    print(f"E: {dict(sorted(elfs.items()))}")


def outcome(rounds, winners):
    return rounds * sum(winners.values())


def round(grid, goblins, elfs, damage):
    units = round_turns(goblins, elfs)
    for unit in units:
        if not goblins or not elfs:
            return True

        if unit not in goblins and unit not in elfs:
            continue

        if can_attack(grid, unit, goblins, elfs):
            attack(grid, unit, goblins, elfs, damage)
        else:
            moved_to = move(grid, unit, goblins, elfs)
            if moved_to and can_attack(grid, moved_to, goblins, elfs):
                attack(grid, moved_to, goblins, elfs, damage)
    return False


def round_turns(goblins, elfs):
    units = list(goblins.keys()) + list(elfs.keys())
    return sorted(units)


def can_attack(grid, unit, goblins, elfs):
    row, col = unit
    type = grid[row][col]
    enemies = goblins if type == "E" else elfs

    if any((nr, nc) in enemies for (nr, nc) in neighbors(grid, row, col)):
        return True
    return False


def attack(grid, unit, goblins, elfs, damage):
    row, col = unit
    type = grid[row][col]
    targets = get_attack_targets(grid, unit, goblins, elfs)
    target = targets[0]
    enemies = goblins if type == "E" else elfs
    enemies[target] -= damage[type]
    if enemies[target] <= 0:
        del enemies[target]
        grid[target[0]][target[1]] = "."


def get_attack_targets(grid, unit, goblins, elfs):
    row, col = unit
    type = grid[row][col]
    enemies = goblins if type == "E" else elfs
    in_range = [
        (nr, nc) for (nr, nc) in neighbors(grid, row, col) if (nr, nc) in enemies
    ]
    return sorted(in_range, key=lambda u: (enemies[u], u))


def move(grid, unit, goblins, elfs):
    row, col = unit
    targets = get_targets(grid, unit, goblins, elfs)
    if not targets:
        return
    paths = search(grid, unit, targets)
    # print(f"ps: {paths}")
    if not paths:
        return
    paths = sorted(paths, key=itemgetter(0))
    target = paths[0][0]

    type = grid[row][col]
    friends = goblins if type == "G" else elfs

    grid[target[0]][target[1]] = grid[row][col]
    friends[target] = friends[unit]

    del friends[unit]
    grid[row][col] = "."
    return target


def get_targets(grid, unit, goblins, elfs):
    row, col = unit
    type = grid[row][col]
    targets = set()
    enemies = goblins if type == "E" else elfs
    for er, ec in enemies:
        for nr, nc in neighbors(grid, er, ec):
            if grid[nr][nc] == ".":
                targets.add((nr, nc))
    return targets


def search(grid, unit, targets):
    queue = deque([])
    queue.append((unit, [unit], 0))
    seen = set()
    solutions = []
    minlen = None

    while queue:
        (row, col), path, steps = queue.popleft()

        if minlen and steps > minlen:
            continue

        if (row, col) in targets:
            if not minlen or steps < minlen:
                minlen = steps
            solutions.append((steps, path))

        if (row, col) in seen:
            continue

        seen.add((row, col))

        for (nr, nc) in neighbors(grid, row, col):
            if (nr, nc) not in seen and grid[nr][nc] == ".":
                queue.append(((nr, nc), path + [(nr, nc)], steps + 1))

    if not solutions:
        return []

    shortest = min(length for length, _ in solutions)

    return [path[1:] for length, path in solutions if length == shortest]


def neighbors(grid, row, col):
    H = len(grid)
    W = len(grid[0])
    res = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if abs(dr) != abs(dc) and 0 <= row + dr < H and 0 <= col + dc < W:
                res.append((row + dr, col + dc))
    return res


def simulate(grid, goblins, elfs):
    d = 4
    while True:
        rounds, winners, type = play(
            deepcopy(grid), deepcopy(goblins), deepcopy(elfs), damage={"G": 3, "E": d}
        )

        if type == "E" and len(winners) == len(elfs):
            return rounds, winners

        d += 1


def main():
    grid, goblins, elfs = parse()
    display(grid)
    rounds, winners, _ = play(deepcopy(grid), deepcopy(goblins), deepcopy(elfs), DAMAGE)
    print(f"Part 1: {outcome(rounds, winners)}")
    rounds, winners = simulate(grid, goblins, elfs)
    print(f"Part 2: {outcome(rounds, winners)}")


if __name__ == "__main__":
    main()
