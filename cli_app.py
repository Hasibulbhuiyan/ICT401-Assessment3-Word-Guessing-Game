"""
ICT401 Assessment 3 - Command Line Interface
Student: Md Hasibul Islam Bhuiyan
Student ID: 202673673
"""

from datetime import datetime
from engine import GameEngine, WordDataError

HISTORY_FILE = "game_history.txt"


def save_history(engine, interface="CLI"):
    """Append one completed session to persistent storage."""
    if not engine.is_finished():
        return

    timestamp = datetime.now().isoformat(timespec="seconds")
    row = (
        f"{timestamp}|{interface}|{engine.secret_word}|"
        f"{engine.result_text()}|{engine.score}|{engine.remaining_lives}\n"
    )
    with open(HISTORY_FILE, "a", encoding="utf-8") as history:
        history.write(row)


def play_game():
    """Run one interactive CLI game."""
    engine = GameEngine("words.txt")

    try:
        engine.select_word()
    except WordDataError as exc:
        print(f"Data error: {exc}")
        return

    print("\n=== ICT401 WORD GUESSING GAME ===")
    print(f"Hint: {engine.hint}")
    print(f"Lives: {engine.remaining_lives}")

    while not engine.is_finished():
        print(f"\nWord: {engine.hidden_word()}")
        print(f"Guessed: {', '.join(sorted(engine.guessed_letters)) or 'None'}")
        print(f"Lives: {engine.remaining_lives} | Score: {engine.score}")

        guess = input("Enter one letter (or Q to quit): ").strip()
        if guess.upper() == "Q":
            print("Game cancelled before completion.")
            return

        result = engine.validate_letter(guess)
        print(result["message"])

        if result["status"] == "invalid":
            print("Example of validation: numbers and symbols are rejected.")
        elif result["status"] == "duplicate":
            print("Choose a letter you have not used before.")

    print(f"\n=== {engine.result_text()} ===")
    print(f"Word: {engine.secret_word}")
    print(f"Final score: {engine.score}")
    save_history(engine, "CLI")


def main():
    """Keep the CLI available for repeated games."""
    while True:
        play_game()
        again = input("\nPlay another game? (Y/N): ").strip().upper()
        if again != "Y":
            print("Thank you for playing.")
            break


if __name__ == "__main__":
    main()
