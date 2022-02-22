import fileinput


def parse():
    return fileinput.input().readline().strip()


def react(polymer):
    stack = []
    for a in polymer:
        if stack and reacts(a, stack[-1]):
            stack.pop()
        else:
            stack.append(a)
    return stack


def reacts(a, b):
    return a != b and a.lower() == b.lower()


def search(polymer):
    units = set(u.lower() for u in polymer)
    minlen = None
    for unit in units:
        curr = "".join([u for u in polymer if u.lower() != unit])
        reacted = react(curr)
        if not minlen or len(reacted) < minlen:
            minlen = len(reacted)
    return minlen


def main():
    polymer = parse()
    reacted = react(polymer)
    print(f"Part 1: {len(reacted)}")
    minlen = search(polymer)
    print(f"Part 2: {minlen}")


if __name__ == "__main__":
    main()
