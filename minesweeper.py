import random
import tkinter as tk
from tkinter import messagebox


class Minesweeper(tk.Frame):
    """A simple Minesweeper implementation using Tkinter."""

    def __init__(self, master=None, rows=10, columns=10, mines=10):
        super().__init__(master)
        self.master = master or tk.Tk()
        self.master.title("Minesweeper")
        self.rows = rows
        self.columns = columns
        self.total_mines = mines
        self.flags_remaining = mines

        self.status_var = tk.StringVar()
        self.status_var.set(f"Flags remaining: {self.flags_remaining}")

        self.header = tk.Frame(self.master)
        self.header.pack(pady=10)

        self.reset_button = tk.Button(
            self.header,
            text="Restart",
            width=10,
            command=self.reset_game,
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(
            self.header,
            textvariable=self.status_var,
            width=20,
            anchor="w",
        )
        self.status_label.pack(side=tk.LEFT, padx=5)

        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack(padx=10, pady=10)

        self.buttons = []
        self.board = []
        self.revealed = set()
        self.flags = set()

        self.create_board()
        self.populate_mines()
        self.update_counts()
        self.create_widgets()

    def create_board(self):
        self.board = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.revealed.clear()
        self.flags.clear()

    def populate_mines(self):
        positions = [(r, c) for r in range(self.rows) for c in range(self.columns)]
        random.shuffle(positions)
        for r, c in positions[: self.total_mines]:
            self.board[r][c] = "M"

    def update_counts(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.board[r][c] == "M":
                    continue
                self.board[r][c] = self.count_adjacent_mines(r, c)

    def create_widgets(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for r in range(self.rows):
            row_buttons = []
            for c in range(self.columns):
                button = tk.Button(
                    self.board_frame,
                    width=2,
                    height=1,
                    command=lambda r=r, c=c: self.on_left_click(r, c),
                )
                button.grid(row=r, column=c)
                button.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                button.bind("<Button-2>", lambda e, r=r, c=c: self.on_right_click(r, c))
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def reset_game(self):
        self.flags_remaining = self.total_mines
        self.status_var.set(f"Flags remaining: {self.flags_remaining}")
        self.create_board()
        self.populate_mines()
        self.update_counts()
        self.create_widgets()

    def count_adjacent_mines(self, row, col):
        count = 0
        for r in range(max(0, row - 1), min(self.rows, row + 2)):
            for c in range(max(0, col - 1), min(self.columns, col + 2)):
                if (r, c) != (row, col) and self.board[r][c] == "M":
                    count += 1
        return count

    def on_left_click(self, row, col):
        if (row, col) in self.flags or (row, col) in self.revealed:
            return
        cell_value = self.board[row][col]
        button = self.buttons[row][col]

        if cell_value == "M":
            button.config(text="💣", disabledforeground="red")
            self.reveal_all_mines()
            self.game_over(False)
            return

        self.reveal_cell(row, col)
        self.check_win_condition()

    def on_right_click(self, row, col):
        button = self.buttons[row][col]
        if (row, col) in self.revealed:
            return
        if (row, col) in self.flags:
            self.flags.remove((row, col))
            button.config(text="")
            self.flags_remaining += 1
        else:
            if self.flags_remaining == 0:
                return
            self.flags.add((row, col))
            button.config(text="🚩")
            self.flags_remaining -= 1
        self.status_var.set(f"Flags remaining: {self.flags_remaining}")

    def reveal_cell(self, row, col):
        if (row, col) in self.revealed or (row, col) in self.flags:
            return

        button = self.buttons[row][col]
        value = self.board[row][col]
        self.revealed.add((row, col))
        button.config(relief=tk.SUNKEN, state=tk.DISABLED)

        if value == 0:
            button.config(text="")
            for nr in range(max(0, row - 1), min(self.rows, row + 2)):
                for nc in range(max(0, col - 1), min(self.columns, col + 2)):
                    if (nr, nc) != (row, col):
                        self.reveal_cell(nr, nc)
        else:
            button.config(text=str(value), disabledforeground=self.get_color(value))

    def get_color(self, value):
        colors = {
            1: "blue",
            2: "green",
            3: "red",
            4: "purple",
            5: "maroon",
            6: "turquoise",
            7: "black",
            8: "gray",
        }
        return colors.get(value, "black")

    def reveal_all_mines(self):
        for r in range(self.rows):
            for c in range(self.columns):
                if self.board[r][c] == "M":
                    button = self.buttons[r][c]
                    button.config(text="💣", disabledforeground="red")
                    button.config(relief=tk.SUNKEN, state=tk.DISABLED)

    def game_over(self, won):
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.config(state=tk.DISABLED)
        if won:
            messagebox.showinfo("Minesweeper", "Congratulations! You cleared the field!")
        else:
            messagebox.showinfo("Minesweeper", "Boom! You hit a mine.")

    def check_win_condition(self):
        if len(self.revealed) == self.rows * self.columns - self.total_mines:
            self.game_over(True)


def main():
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()


if __name__ == "__main__":
    main()
