import fileinput


def parse():
    return [int(line.strip()) for line in fileinput.input()]


def search(diffs):
    curr = 0
    seen = set()

    while True:
        for diff in diffs:
            curr += diff
            if curr in seen:
                return curr
            seen.add(curr)


def main():
    diffs = parse()
    print(f"Part 1: {sum(diffs)}")
    twice = search(diffs)
    print(f"Part 2: {twice}")


if __name__ == "__main__":
    main()
