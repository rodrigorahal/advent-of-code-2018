def run(recipes):
    board = [3, 7]
    fst = 0
    snd = 1

    while len(board) < recipes + 10:
        score = board[fst] + board[snd]
        digits = map(int, str(score))
        board.extend(digits)

        fst = (fst + 1 + board[fst]) % len(board)
        snd = (snd + 1 + board[snd]) % len(board)

    return board


def run_with_target(target):
    board = [3, 7]
    fst = 0
    snd = 1

    n = len(target)
    i = 0

    while True:
        score = board[fst] + board[snd]
        digits = map(int, str(score))
        board.extend(digits)

        fst = (fst + 1 + board[fst]) % len(board)
        snd = (snd + 1 + board[snd]) % len(board)

        if get_score(board[i : i + n]) == target:
            return i

        i += 1


def get_score(board):
    return "".join(map(str, board))


def main():
    RECIPES = 320851
    board = run(RECIPES)
    scores = "".join(map(str, board[RECIPES : RECIPES + 10]))
    print(f"Part 1: {scores}")

    TARGET = "320851"
    recipes = run_with_target(TARGET)
    print(f"Part 2: {recipes}")


if __name__ == "__main__":
    main()
