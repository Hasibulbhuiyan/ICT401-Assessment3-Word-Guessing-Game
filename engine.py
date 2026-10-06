"""
ICT401 Assessment 3 - Core Game Logic
Student: Md Hasibul Islam Bhuiyan
Student ID: 202673673

The GameEngine contains game rules only. It does not use print() or input().
"""

from pathlib import Path
import random


class WordDataError(Exception):
    """Raised when an external word data file cannot be read correctly."""


class GameEngine:
    """Core logic for the word-guessing game."""

    def __init__(self, data_file="words.txt", lives=6):
        self.data_file = Path(data_file)
        self.max_lives = lives
        self.secret_word = ""
        self.hint = ""
        self.guessed_letters = set()
        self.remaining_lives = lives
        self.score = 0
        self.won = False
        self.lost = False

    def _load_words(self):
        """Load WORD|Hint records from the external file."""
        if not self.data_file.exists():
            raise WordDataError(f"Word source file not found: {self.data_file}")

        records = []
        try:
            for line_number, raw_line in enumerate(
                self.data_file.read_text(encoding="utf-8").splitlines(), start=1
            ):
                line = raw_line.strip()
                if not line:
                    continue
                if "|" not in line:
                    raise WordDataError(
                        f"Invalid record on line {line_number}: expected WORD|Hint"
                    )
                word, hint = line.split("|", 1)
                word = word.strip().upper()
                hint = hint.strip()
                if not word.isalpha() or not hint:
                    raise WordDataError(
                        f"Invalid record on line {line_number}: word/hint is empty or invalid"
                    )
                records.append((word, hint))
        except OSError as exc:
            raise WordDataError(f"Could not read word source: {exc}") from exc

        if not records:
            raise WordDataError("The word source file contains no valid records.")
        return records

    def select_word(self):
        """Select a new random word and reset the game state."""
        records = self._load_words()
        self.secret_word, self.hint = random.choice(records)
        self.guessed_letters = set()
        self.remaining_lives = self.max_lives
        self.score = 0
        self.won = False
        self.lost = False
        return self.secret_word

    def validate_letter(self, letter):
        """
        Validate and process one guess.
        Returns a dictionary describing the result.
        """
        if self.won or self.lost:
            return {"status": "finished", "message": "The game has already ended."}

        if not isinstance(letter, str) or len(letter.strip()) != 1:
            return {"status": "invalid", "message": "Please enter exactly one letter."}

        letter = letter.strip().upper()
        if not letter.isalpha() or len(letter) != 1:
            return {"status": "invalid", "message": "Only letters A-Z are accepted."}

        if letter in self.guessed_letters:
            return {"status": "duplicate", "message": f"You already guessed '{letter}'."}

        self.guessed_letters.add(letter)

        if letter in self.secret_word:
            self.score += 10
            if all(ch in self.guessed_letters for ch in self.secret_word):
                self.won = True
                self.score += self.remaining_lives * 5
                return {"status": "win", "message": "Correct! You solved the word."}
            return {"status": "correct", "message": "Correct guess."}

        self.remaining_lives -= 1
        if self.remaining_lives <= 0:
            self.lost = True
            return {"status": "loss", "message": f"Game over. The word was {self.secret_word}."}
        return {"status": "incorrect", "message": "Incorrect guess."}

    def hidden_word(self):
        """Return the word with unguessed letters hidden."""
        return " ".join(
            ch if ch in self.guessed_letters else "_"
            for ch in self.secret_word
        )

    def is_finished(self):
        return self.won or self.lost

    def result_text(self):
        if self.won:
            return "WIN"
        if self.lost:
            return "LOSS"
        return "IN PROGRESS"
