from audioop import maxpp
from dis import dis
import fileinput


def parse():
    first = True
    rules = dict()
    for line in fileinput.input():
        if first:
            state = dict(enumerate(line.strip().strip("initial state: ")))
            first = False
        else:
            if line != "\n":
                rule, outcome = line.strip().split(" => ")
                rules[rule] = outcome
    return state, rules


def run(state, rules, gens=20):
    curr_state = state
    for gen in range(gens):
        # display(curr_state, -50, 50)
        new_state = dict()
        plnts = [k for k, v in curr_state.items() if v == "#"]
        minp, maxp = min(plnts), max(plnts)
        for i in range(minp - 10, maxp + 10):
            p = pattern(curr_state, i)
            new_state[i] = rules.get(p, ".")
        curr_state = new_state

        # print(gen, minp, maxp, maxp - minp, plants(curr_state))
        # print(gen - minp, gen - maxp)
        # display(curr_state, minp, maxp)
        # print(f"relative: {[k-minp for k in plnts]}")

        # print(gen, plants(curr_state), min(plnts), max(plnts))
    return curr_state


"""
minp = gen - 41
maxp = gen + 96

"""


def plants(state):
    return sum(pot for pot, plant in state.items() if plant == "#")


def pattern(state, curr):
    return "".join(state.get(i, ".") for i in range(curr - 2, curr + 3))


def display(state, start, end):
    print("".join(state.get(i, ".") for i in range(start, end)))


def main():
    state, rules = parse()

    final_state = run(state, rules)
    print(f"Part 1: {plants(final_state)}")

    # After some exploration of the state evolution after a few generations
    # I noticed the state ~stabalizes relatively to the min pot with a plant at the following configuration:
    # .###.......###.........#...###.....###.#....#.###..#...#....#...#.#.......#.#..............................#
    # This is known as a glider in Conway's game of life lingo https://en.wikipedia.org/wiki/Glider_(Conway%27s_Life)
    # I also found that, after stabilization, the min pot is equal to GENERATION - 41
    # and the relative postions to min pot are:
    relative = [
        0,
        1,
        2,
        12,
        13,
        14,
        25,
        26,
        27,
        78,
        79,
        80,
        90,
        91,
        92,
        100,
        101,
        102,
        135,
        136,
        137,
    ]

    minpot = 50_000_000_000 - 41

    print(f"Part 2: {sum(r + minpot for r in relative)}")


if __name__ == "__main__":
    main()
