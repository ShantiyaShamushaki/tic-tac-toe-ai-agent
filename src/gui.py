import tkinter as tk
from tkinter import messagebox
from .game_logic import Game


class TicTacToeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe | Minimax AI")

        self.game = Game()
        self.player_symbol = None
        self.ai_symbol = None
        self.stats = {"win": 0, "loss": 0, "draw": 0}

        # --- Header ---
        self.header = tk.Label(self.root, text="Select your symbol", font=("Arial", 14))
        self.header.grid(row=0, column=0, columnspan=3, pady=(10, 5))

        # --- Status (turn info) ---
        self.status_label = tk.Label(self.root, text="Waiting for selection...", font=("Arial", 11))
        self.status_label.grid(row=1, column=0, columnspan=3, pady=(0, 5))

        # --- Symbol selection frame ---
        self.choice_frame = tk.Frame(self.root)
        self.choice_frame.grid(row=2, column=0, columnspan=3, pady=5)
        tk.Button(self.choice_frame, text="Play as X", font=("Arial", 12),
                  command=lambda: self.choose_symbol(1)).grid(row=0, column=0, padx=5)
        tk.Button(self.choice_frame, text="Play as O", font=("Arial", 12),
                  command=lambda: self.choose_symbol(0)).grid(row=0, column=1, padx=5)

        # --- Game Grid ---
        self.buttons = [[None]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                b = tk.Button(self.root, text="", width=5, height=2,
                              font=("Arial", 24), state="disabled",
                              command=lambda r=i, c=j: self.on_click(r, c))
                b.grid(row=i+3, column=j)
                self.buttons[i][j] = b

        # --- Stats and Restart ---
        self.stats_label = tk.Label(self.root, text="", font=("Arial", 11))
        self.stats_label.grid(row=6, column=0, columnspan=3, pady=5)

        self.restart_btn = tk.Button(self.root, text="Restart", font=("Arial", 12),
                                     bg="#dcdcdc", command=self.reset_game)
        self.restart_btn.grid(row=7, column=0, columnspan=3, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)
        self._update_stats()

    # ----------------------------------------------------
    def choose_symbol(self, symbol):
        if any(cell is not None for row in self.game.map for cell in row):
            messagebox.showwarning("Invalid Action", "You can change symbol only before starting a new game.")
            return

        # ست کردن سمبل‌ها
        self.player_symbol = symbol
        self.ai_symbol = 1 if symbol == 0 else 0

        # ریست کامل بازی
        self.game.reset()
        self.enable_board(True)
        self.update_ui()

        self.header.config(text=f"You are {'X' if symbol == 1 else 'O'}")
        self.status_label.config(text="Your turn" if symbol == 1 else "AI starts")

        if symbol == 0:
            self.game.turn = self.ai_symbol
            self.game.ai_move()
            self.game.change_turn()
            self.update_ui()
            self.status_label.config(text="Your turn")

    def on_click(self, r, c):
        if self.game.map[r][c] is not None or self.player_symbol is None:
            return
        self.game.map[r][c] = self.player_symbol
        self.update_ui()

        result = self.game.check_winner()
        if self._handle_result(result): return

        self.game.change_turn()
        self.status_label.config(text="AI thinking…")
        self.root.update_idletasks()
        self.game.ai_move()
        self.update_ui()
        result = self.game.check_winner()
        if self._handle_result(result): return

        self.game.change_turn()
        self.status_label.config(text="Your turn")

    # ----------------------------------------------------
    def _handle_result(self, result):
        if result is None: return False

        if result == 100: winner = 1
        elif result == -100: winner = 0
        else: winner = None

        if winner == self.player_symbol:
            messagebox.showinfo("Result", "You won! 🎉")
            self.stats["win"] += 1
        elif winner == self.ai_symbol:
            messagebox.showinfo("Result", "You lost 😔")
            self.stats["loss"] += 1
        else:
            messagebox.showinfo("Result", "Draw ⚖️")
            self.stats["draw"] += 1

        self.game.reset()
        self.update_ui()
        self.status_label.config(text="Your turn")
        self._update_stats()
        return True

    # ----------------------------------------------------
    def update_ui(self):
        for i in range(3):
            for j in range(3):
                val = self.game.map[i][j]
                btn = self.buttons[i][j]
                if val == 1:
                    btn.config(text="X", state="disabled")
                elif val == 0:
                    btn.config(text="O", state="disabled")
                else:
                    btn.config(text="", state="normal")

    def enable_board(self, enable=True):
        state = "normal" if enable else "disabled"
        for row in self.buttons:
            for btn in row:
                btn.config(state=state)

    def reset_game(self):
        if self.player_symbol is None:
            messagebox.showwarning("Error", "Please select X or O first")
            return
        self.game.reset()
        self.update_ui()
        self.status_label.config(text="Your turn")
        self._update_stats()

    def _update_stats(self):
        self.stats_label.config(
            text=f"Wins: {self.stats['win']} | Losses: {self.stats['loss']} | Draws: {self.stats['draw']}"
        )

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    TicTacToeGUI().run()
