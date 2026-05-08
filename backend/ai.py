def best_move(board, ai="O", human="X"):
    EMPTY = ""

    wins = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    def winner(b):
        for a, c, d in wins:
            if b[a] != EMPTY and b[a] == b[c] == b[d]:
                return b[a]

        if EMPTY not in b:
            return "draw"

        return None

    def minimax(b, is_ai_turn):
        result = winner(b)

        if result == ai:
            return 1
        if result == human:
            return -1
        if result == "draw":
            return 0

        if is_ai_turn:
            best_score = -float("inf")

            for i in range(9):
                if b[i] == EMPTY:
                    b[i] = ai
                    score = minimax(b, False)
                    b[i] = EMPTY
                    best_score = max(best_score, score)

            return best_score

        else:
            best_score = float("inf")

            for i in range(9):
                if b[i] == EMPTY:
                    b[i] = human
                    score = minimax(b, True)
                    b[i] = EMPTY
                    best_score = min(best_score, score)

            return best_score

    best_score = -float("inf")
    best_index = None

    for i in range(9):
        if board[i] == EMPTY:
            board[i] = ai
            score = minimax(board, False)
            board[i] = EMPTY

            if score > best_score:
                best_score = score
                best_index = i

    return best_index