"""
ICT401 Assessment 3 - Tkinter Graphical User Interface
Student: Md Hasibul Islam Bhuiyan
Student ID: 202673673

The GUI imports the exact same GameEngine used by the CLI.
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from engine import GameEngine, WordDataError

HISTORY_FILE = "game_history.txt"


class WordGuessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ICT401 Word Guessing Game")
        self.root.geometry("720x620")
        self.root.resizable(False, False)

        self.engine = GameEngine("words.txt")
        self.buttons = {}

        self.title_label = tk.Label(
            root, text="WORD GUESSING GAME",
            font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=15)

        self.hint_label = tk.Label(root, text="", font=("Arial", 12))
        self.hint_label.pack(pady=5)

        self.word_label = tk.Label(
            root, text="", font=("Consolas", 28, "bold")
        )
        self.word_label.pack(pady=20)

        self.status_label = tk.Label(root, text="", font=("Arial", 13))
        self.status_label.pack(pady=5)

        self.lives_label = tk.Label(root, text="", font=("Arial", 13))
        self.lives_label.pack(pady=5)

        keyboard = tk.Frame(root)
        keyboard.pack(pady=20)

        for index, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            button = tk.Button(
                keyboard,
                text=letter,
                width=4,
                height=2,
                command=lambda l=letter: self.make_guess(l)
            )
            button.grid(row=index // 9, column=index % 9, padx=3, pady=3)
            self.buttons[letter] = button

        self.new_button = tk.Button(
            root, text="New Game", width=15,
            command=self.new_game
        )
        self.new_button.pack(pady=10)

        self.new_game()

    def new_game(self):
        try:
            self.engine.select_word()
        except WordDataError as exc:
            messagebox.showerror("Word Data Error", str(exc))
            return

        for button in self.buttons.values():
            button.config(state="normal")

        self.update_display()

    def make_guess(self, letter):
        result = self.engine.validate_letter(letter)

        # A clicked keyboard button is disabled so repeated GUI clicks
        # cannot submit the same letter again.
        self.buttons[letter].config(state="disabled")
        self.update_display()

        if result["status"] == "win":
            self.finish_game("You won!")
        elif result["status"] == "loss":
            self.finish_game(f"You lost. The word was {self.engine.secret_word}.")
        elif result["status"] == "invalid":
            messagebox.showwarning("Invalid Input", result["message"])

    def update_display(self):
        self.word_label.config(text=self.engine.hidden_word())
        self.hint_label.config(text=f"Hint: {self.engine.hint}")
        self.lives_label.config(
            text=f"Remaining lives: {'♥ ' * self.engine.remaining_lives}"
        )
        self.status_label.config(
            text=f"Score: {self.engine.score} | Guessed: "
                 f"{', '.join(sorted(self.engine.guessed_letters)) or 'None'}"
        )

    def finish_game(self, message):
        self.update_display()
        self.save_history()
        for button in self.buttons.values():
            button.config(state="disabled")
        messagebox.showinfo("Game Result", message)

    def save_history(self):
        timestamp = datetime.now().isoformat(timespec="seconds")
        row = (
            f"{timestamp}|GUI|{self.engine.secret_word}|"
            f"{self.engine.result_text()}|{self.engine.score}|"
            f"{self.engine.remaining_lives}\n"
        )
        with open(HISTORY_FILE, "a", encoding="utf-8") as history:
            history.write(row)


if __name__ == "__main__":
    root = tk.Tk()
    app = WordGuessGUI(root)
    root.mainloop()
