import customtkinter as ctk
import random

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")
        self.master.geometry("400x500")
        self.master.configure(padx=10, pady=10)

        self.board = [""] * 9
        self.buttons = []
        self.status_label = None
        self.current_player = "X"  # Human always starts

        self.create_widgets()

    def create_widgets(self):
        grid_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        grid_frame.pack(pady=20)

        for i in range(9):
            button = ctk.CTkButton(grid_frame,
                                   text="",
                                   font=("Segoe UI", 36, "bold"),
                                   width=100,
                                   height=100,
                                   fg_color="#e0f7fa",
                                   text_color_disabled="gray",
                                   corner_radius=10,
                                   command=lambda i=i: self.human_move(i))
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

        self.status_label = ctk.CTkLabel(self.master,
                                         text="",
                                         font=("Segoe UI", 20),
                                         text_color="green")
        self.status_label.pack(pady=10)

        self.reset_button = ctk.CTkButton(self.master,
                                          text="Restart Game",
                                          font=("Segoe UI", 16),
                                          command=self.reset_game)
        self.reset_button.pack(pady=10)

    def human_move(self, index):
        if self.board[index] == "" and not self.check_winner():
            self.make_move(index, "X")
            if not self.check_winner() and "" in self.board:
                self.master.after(400, self.computer_move)

    def computer_move(self):
        index = self.find_best_move()
        if index is not None:
            self.make_move(index, "O")

    def make_move(self, index, player):
        self.board[index] = player
        color = "#0288d1" if player == "X" else "#d32f2f"
        self.buttons[index].configure(text=player, text_color=color, state="disabled")
        if self.check_winner():
            self.announce_winner(player)
        elif "" not in self.board:
            self.announce_tie()

    def check_winner(self):
        wins = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                (0, 4, 8), (2, 4, 6)]
        for a, b, c in wins:
            if self.board[a] == self.board[b] == self.board[c] != "":
                return True
        return False

    def announce_winner(self, winner):
        self.status_label.configure(text=f"Player {winner} wins!",
                                    text_color="green" if winner == "X" else "red")
        self.disable_all_buttons()

    def announce_tie(self):
        self.status_label.configure(text="It's a tie!", text_color="purple")
        self.disable_all_buttons()

    def disable_all_buttons(self):
        for btn in self.buttons:
            btn.configure(state="disabled")

    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        for btn in self.buttons:
            btn.configure(text="", state="normal", text_color="black", fg_color="#e0f7fa")
        self.status_label.configure(text="")

    def find_best_move(self):
        # Check for winning move
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                if self.check_winner():
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        # Check for blocking move
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"
                if self.check_winner():
                    self.board[i] = ""
                    return i
                self.board[i] = ""

        # Otherwise, pick random available spot
        available = [i for i, cell in enumerate(self.board) if cell == ""]
        return random.choice(available) if available else None


if __name__ == "__main__":
    root = ctk.CTk()
    app = TicTacToe(root)
    root.mainloop()
