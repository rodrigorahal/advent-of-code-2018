def get_subgrid(row, col, size):
    if row > (300 - size + 1) or col > (300 - size + 1):
        return []
    subgrid = []
    for dr in range(size):
        subrow = [(row + dr, col + dc) for dc in range(size)]
        subgrid.append(subrow)
    return subgrid


def power(X, Y, serial):
    rack = X + 10
    level = rack * Y
    level += serial
    level *= rack
    if level < 100:
        return -5
    return int(str(level)[-3]) - 5


def grid_power(grid, serial):
    level = 0
    for row in grid:
        for (Y, X) in row:
            level += power(X, Y, serial)
    return level


def row_power(grid, row, col, size, serial):
    return sum(
        power(X, Y, serial) for (Y, X) in grid[row - 1][col - 1 : col - 1 + size]
    )


def col_power(grid, row, col, size, serial):
    X = col
    return sum(power(X, Y, serial) for Y in range(row, row + size))


def display(grid):
    for row in grid:
        print(" ".join(str(v) for v in row))
    print()


def search(serial):
    powers = dict()
    for row in range(1, 209):
        for col in range(1, 209):
            grid = get_subgrid(row, col, 3)
            powers[(row, col)] = grid_power(grid, serial)
    return max([(v, k) for k, v in powers.items()])


def search_with_grid(grid, serial):
    highest = 0
    corner = None

    for row in range(1, 300):
        for col in range(1, 300):
            maxsize = min((301 - row), (301 - col))
            level = power(col, row, serial)
            if not corner or level > highest:
                highest = level
                corner = row, col, 1
            for size in range(2, maxsize):
                level += row_power(grid, row + size - 1, col, size, serial)
                level += col_power(grid, row, col + size - 1, size, serial)
                level -= power(col + size - 1, row + size - 1, serial)

                if level > highest:
                    highest = level
                    corner = row, col, size
    return corner


def main():
    SERIAL = 1308
    level, (row, col) = search(SERIAL)
    print(f"Part 1: {col, row}")

    grid = get_subgrid(1, 1, 300)
    row, col, size = search_with_grid(grid, SERIAL)
    print(f"Part 2: {col, row, size}")


if __name__ == "__main__":
    main()
