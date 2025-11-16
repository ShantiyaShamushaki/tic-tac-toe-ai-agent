# game_logic.py
from itertools import chain

class Game:
    def __init__(self):
        self.map = [[None] * 3 for _ in range(3)]
        self.turn = 1  # 1 = X, 0 = O

    def reset(self):
        self.map = [[None] * 3 for _ in range(3)]
        self.turn = 1

    def change_turn(self):
        self.turn = 1 if self.turn == 0 else 0

    def available_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.map[i][j] is None]

    def rows(self): return self.map
    def columns(self): return [[self.map[r][c] for r in range(3)] for c in range(3)]
    def diagonals(self):
        return [[self.map[i][i] for i in range(3)],
                [self.map[i][2-i] for i in range(3)]]

    def check_winner(self):
        have_move = any(cell is None for row in self.map for cell in row)
        for sqe in chain(self.rows(), self.columns(), self.diagonals()):
            if sqe.count(1) == 3:
                return 100
            if sqe.count(0) == 3:
                return -100
        return None if have_move else 0  # draw or continue

    def evaluate(self, depth=0, is_maximizer=False, alpha=float('-inf'), beta=float('inf')):
        result = self.check_winner()
        if result is not None:
            # tie-breaking: prefer faster wins, slower losses
            if result > 0:
                return result + (10 - depth)
            elif result < 0:
                return result - (10 - depth)
            else:
                return 0

        if is_maximizer:
            max_eval = float('-inf')
            for i, j in self.available_moves():
                self.map[i][j] = 1
                eval_child = self.evaluate(depth + 1, False, alpha, beta)
                self.map[i][j] = None
                max_eval = max(max_eval, eval_child)
                alpha = max(alpha, eval_child)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for i, j in self.available_moves():
                self.map[i][j] = 0
                eval_child = self.evaluate(depth + 1, True, alpha, beta)
                self.map[i][j] = None
                min_eval = min(min_eval, eval_child)
                beta = min(beta, eval_child)
                if beta <= alpha:
                    break
            return min_eval

    def ai_move(self):
        best_move = None
        if self.turn == 1:  # AI is X
            best_score = float('-inf')
            for i, j in self.available_moves():
                self.map[i][j] = 1
                score = self.evaluate(0, is_maximizer=False)
                self.map[i][j] = None
                if score > best_score:
                    best_score, best_move = score, (i, j)
        else:  # AI is O
            best_score = float('inf')
            for i, j in self.available_moves():
                self.map[i][j] = 0
                score = self.evaluate(0, is_maximizer=True)
                self.map[i][j] = None
                if score < best_score:
                    best_score, best_move = score, (i, j)
        if best_move:
            i, j = best_move
            self.map[i][j] = self.turn
