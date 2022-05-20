import tkinter as tk
import tkinter.ttk as ttk
from wordle import Wordle
from guesser import Guesser

class Game_GUI(object):
    def __init__(self):
        self.window = tk.Tk()
        self.frame = []
        self.game = []
        self.play_area_frame = ttk.Frame(master = self.window)

    def ask_which_game(self):
        for widget in self.window.grid_slaves():
            widget.destroy()
        self.window.title("Wordle/Quordle Solver")
        self.window.resizable(False, False)
        wordle_button = ttk.Button(
            text = "Wordle",
            command = self.wordle_game
        ).grid(column = 0, row = 0)
        quordle_button = ttk.Button(
            text = "Quordle",
            command = self.quordle_game
        ).grid(column = 1, row = 0)

    def play_game(self):
        self.window.mainloop()

    def clean_screen(self, title):
        for widget in self.window.grid_slaves():
            widget.destroy()
        self.window.title(title)

    def wordle_game(self):
        self.clean_screen("Wordle Solver")
        self.make_game_frame(0, 0, shared = False)
        self.play_area_frame.pack()

    def quordle_game(self):
        self.clean_screen("Quorlde Solver")
        self.main_guess_text = tk.StringVar()
        self.main_guess_text.trace_add("write", lambda unused1, unused2, unused3: self.main_update_buttons(self.main_guess_text))
        self.main_guess_entry = ttk.Entry(master = self.window,
                                     textvariable = self.main_guess_text,
                                     justify = "center",
                                     width = 7)
        self.main_solve_button = ttk.Button(master = self.window,
                                            text = "Solve All",
                                            command = self.solve_all_puzzles)
        self.main_guess_entry.pack()
        self.main_solve_button.pack()
        self.play_area_frame.pack()

        for vertical in range(2):
            for horizontal in range(2):
                self.make_game_frame(horizontal, vertical, shared = True)

    def make_game_frame(self, horizontal, vertical, shared):
        self.frame.append(ttk.Frame(self.play_area_frame,
                                    borderwidth = 5,
                                    relief = tk.GROOVE))
        self.frame[len(self.game)].grid(column = horizontal, row = vertical)
        self.game.append(Game_Space(self.frame[len(self.game)], shared))

    def main_update_buttons(self, textable):
        content = self.main_limit_text_length(self.main_guess_entry, textable, 5)
        for game_instance in self.game:
            for index in range(len(game_instance.position_button)):
                if index < len(content):
                    game_instance.position_button[index]["text"] = content[index]
                else:
                    game_instance.position_button[index]["text"] = ""

    def main_limit_text_length(self, widget, text, length = 5):
        while len(text.get()) > length:
            widget.delete(0)
        return text.get()

    def solve_all_puzzles(self):
        for game_instance in self.game:
            game_instance.solve_puzzle()

class Game_Space(object):
    def __init__(self, frame, shared):
        self.frame = frame
        self.game = Wordle()
        self.game.load_default_word_lists()
        self.guess_text = tk.StringVar()
        self.guess_text.trace_add("write", lambda unused1, unused2, unused3: self.update_buttons(self.guess_text))
        self.guess_entry = ttk.Entry(master = self.frame,
                                     textvariable = self.guess_text,
                                     justify = "center",
                                     width = 7)
        self.buttons_frame = ttk.Frame(master = self.frame)
        self.solve_button = ttk.Button(master = self.frame,
                                       text = "Solve",
                                       command = self.solve_puzzle)
        self.answer_remaining_label = ttk.Label(master = self.frame,
                                                text = f"{len(self.game)} valid answers remain")
        self.guess_remaining_label = ttk.Label(master = self.frame,
                                                text = f"{len(self.game.guess_list)} valid guesses remain")
        self.answer_box = tk.Text(master = self.frame,
                                  wrap = tk.WORD,
                                  width = 21,
                                  height = 5)
        self.suggest_word_button = ttk.Button(master = self.frame,
                                              command = self.suggest_a_word,
                                              text = "Suggest'A'Word")
        self.suggest_word_label = ttk.Label(master = self.frame,
                                            text = "")

        if shared == False:
            self.guess_entry.pack()
        self.buttons_frame.pack()
        if shared == False:
            self.solve_button.pack()
        self.answer_remaining_label.pack()
        self.guess_remaining_label.pack()
        self.answer_box.pack()
        self.suggest_word_button.pack()
        self.suggest_word_label.pack()

        self.position_button = []
        for position in range(5):
            def button_action(number = position):
                return self.multi_clicker(number)

            self.position_button.append(tk.Button(master = self.buttons_frame,
                                                  relief = "groove",
                                                  fg = 'black',
                                                  bg = 'light gray',
                                                  width = 3,
                                                  text = "-",
                                                  command = button_action))
            self.position_button[position].grid(column = position, row = 0)

    def multi_clicker(self, position):
        if self.position_button[position]["background"] == "light gray":
            self.position_button[position]["background"] = "yellow"
        elif self.position_button[position]["background"] == "yellow":
            self.position_button[position]["background"] = "green"
        elif self.position_button[position]["background"] == "green":
            self.position_button[position]["background"] = "light gray"

    def solve_puzzle(self):
        bad_letters = ""
        good_letters = {}
        known_letters = {}

        # Populate the bad/good/known letters into the solve engine
        for index in range(len(self.position_button)):
            if self.position_button[index]["background"] == "light gray":
                bad_letters +=  self.position_button[index]["text"]
            elif self.position_button[index]["background"] == "yellow":
                good_letters[index] =  self.position_button[index]["text"]
            else:
                known_letters[index] =  self.position_button[index]["text"]
            self.position_button[index]["background"] = "light gray"
        self.game.add_bad_letters(bad_letters)
        self.game.add_good_letters(good_letters)
        self.game.add_known_letters(known_letters)
        self.game.solve()

        # List all of the valid answers in the answer box
        self.answer_box["state"] = tk.NORMAL
        self.answer_box.delete("1.0", tk.END)
        self.answer_box.insert(tk.END, f"{self.game}")
        self.answer_box["state"] = tk.DISABLED

        # Update the number of remaining answers label
        if len(self.game) == 1:
            text_to_display = f"1 valid answer remains"
        else:
            text_to_display = f"{len(self.game)} valid answers remain"
        self.answer_remaining_label["text"] = text_to_display

        # Update the number of remaining guesses label
        if len(self.game) == 1:
            text_to_display = f"1 valid guess remains"
        else:
            text_to_display = f"{len(self.game.guess_list)} valid guesses remain"
        self.guess_remaining_label["text"] = text_to_display

        # Clear the guess box and ready it to receive the next guess
        # self.guess_entry.delete(0, tk.END)
        # self.guess_entry.focus()

    def update_buttons(self, textable):
        content = self.limit_text_length(self.guess_entry, textable, 5)
        for index in range(len(self.position_button)):
            if index < len(content):
                self.position_button[index]["text"] = content[index]
            else:
                self.position_button[index]["text"] = ""

    def limit_text_length(self, widget, text, length = 5):
        while len(text.get()) > length:
            widget.delete(0)
        return text.get()

    def suggest_a_word(self):
        best_guess = Guesser(self.game.answer_list, self.game.guess_list)
        best_word = best_guess.sift_through_guesses()
        self.suggest_word_label["text"] = best_word
