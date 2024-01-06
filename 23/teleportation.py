import fileinput
import z3


def count(bots):
    strongest = max(bots, key=lambda b: b[1])
    return sum(is_in_range(strongest, bot) for bot in bots)


def is_in_range(a, b):
    (xa, ya, za), ra = a
    (xb, yb, zb), rb = b

    dist = abs(xb - xa) + abs(yb - ya) + abs(zb - za)
    return dist <= ra


def edges(bots):
    minx = maxx = miny = maxy = minz = maxz = 0
    for (x, y, z), _ in bots:
        minx = min(minx, x)
        maxx = max(maxx, x)
        miny = min(miny, y)
        maxy = max(maxy, y)
        minz = min(minz, z)
        maxz = max(maxz, z)
    return minx, maxx, miny, maxy, minz, maxz


def parse():
    bots = []
    for line in fileinput.input():
        pos, r = line.removeprefix("pos=<").strip().split(", r=")
        r = int(r)
        x, y, z = tuple(map(int, pos.strip("<>").split(",")))
        bots.append(((x, y, z), r))
    return bots


def z3abs(x):
    return z3.If(x >= 0, x, -x)


def solve(bots):
    X, Y, Z = z3.Int("x"), z3.Int("y"), z3.Int("z")
    R = [
        z3abs(X - xi) + z3abs(Y - yi) + z3abs(Z - zi) <= ri for (xi, yi, zi), ri in bots
    ]
    T = sum(R)

    opt = z3.Optimize()
    opt.maximize(T)
    opt.check()
    M = opt.model()
    return M.eval(X + Y + Z)


def main():
    bots = parse()
    print(f"Part 1: {count(bots)}")
    print(f"Part 2: {solve(bots)}")


if __name__ == "__main__":
    main()
