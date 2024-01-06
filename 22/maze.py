from heapq import heappop, heappush

TOOLS = {
    0: ["climbing", "torch"],
    1: ["climbing", "neither"],
    2: ["neither", "torch"],
}


def geologic_index(erosion, x, y, tx, ty):
    if (x, y) == (0, 0):
        return 0
    if (x, y) == (tx, ty):
        return 0
    if y == 0:
        return x * 16807
    if x == 0:
        return y * 48271
    return erosion[x - 1, y] * erosion[x, y - 1]


def erosion_level(erosion, depth, x, y, tx, ty):
    index = geologic_index(erosion, x, y, tx, ty)
    level = (index + depth) % 20183
    erosion[x, y] = level
    return level


def compute(sx, sy, tx, ty, depth, deeper=False):
    erosion = dict()
    types = dict()

    ey = ty + 1_000 if deeper else ty + 1
    ex = tx + 1_000 if deeper else tx + 1

    for y in range(sy, ey):
        for x in range(sx, ex):
            level = erosion_level(erosion, depth, x, y, tx, ty)
            types[x, y] = level % 3
    return erosion, types


def dijsktra(types, sx, sy, tx, ty):
    cost, x, y, tool, path = (0, sx, sy, "torch", ((0, 0, "t")))
    queue = [(cost, x, y, tool, path)]
    seen = set()

    while queue:
        cost, x, y, tool, path = heappop(queue)

        if (x, y, tool) in seen:
            continue

        seen.add((x, y, tool))

        if (x, y) == (tx, ty) and tool == "torch":
            return cost, path

        type = types[x, y]
        (switch,) = [opt for opt in TOOLS[type] if opt != tool]

        for dx, dy in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy

            if nx < 0 or ny < 0:
                continue

            ntype = types[nx, ny]

            # if can move, add to queue with cost + 1
            if tool in TOOLS[ntype]:
                heappush(queue, (cost + 1, nx, ny, tool, path + ((nx, ny, tool[0]),)))

            # if can move after switching tool, add to queue with cost + 7
            if switch in TOOLS[ntype]:
                heappush(
                    queue, (cost + 7 + 1, nx, ny, switch, path + ((nx, ny, switch[0]),))
                )


def main():
    sx, sy = 0, 0
    depth = 5355
    tx, ty = 14, 796

    erosion, types = compute(sx, sy, tx, ty, depth)
    print(f"Part 1: {sum(types.values())}")

    erosion, types = compute(sx, sy, tx, ty, depth, deeper=True)
    cost, path = dijsktra(types, sx, sy, tx, ty)
    print(f"Part 2: {cost}")


if __name__ == "__main__":
    main()
