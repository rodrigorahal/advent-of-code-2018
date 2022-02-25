import fileinput


def parse():
    stars = []
    for line in fileinput.input():
        words = line.strip("position=<").split(" velocity=<")
        position = tuple(map(int, words[0].strip().strip(">").split(", ")))
        velocity = tuple(map(int, words[1].strip().strip(">").split(", ")))
        stars.append((position, velocity))
    return stars


def simulate(stars, steps=10):
    state = stars[:]

    for i in range(1, steps):
        updated_state = []
        for (x, y), (vx, vy) in state:
            updated_state.append(((x + vx, y + vy), (vx, vy)))
        state = updated_state

        if has_message(state):
            display(state)
            return i

    return -1


def display(state):
    xs = [x for (x, y), _ in state]
    ys = [y for (x, y), _ in state]

    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    plot = set((x, y) for (x, y), _ in state)

    print("Part 1:")
    for y in range(miny - 1, maxy + 2):
        print(
            "".join("#" if (x, y) in plot else " " for x in range(minx - 1, maxx + 2))
        )
    print()


def has_message(state):
    xs = [x for (x, y), _ in state]
    minx, maxx = min(xs), max(xs)
    # trial and error
    if maxx - minx <= 61:
        return True
    return False


def main():
    stars = parse()
    steps = simulate(stars, steps=100_000)
    print(f"Part 2: {steps}")


if __name__ == "__main__":
    main()
