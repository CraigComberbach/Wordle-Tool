import tkinter as tk
import tkinter.ttk as ttk
from wordle import Wordle

class Game_GUI(object):
    def __init__(self):
        self.window = tk.Tk()
        self.frame = []
        self.game = []

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
        self.make_game_frame(0, 0)

    def quordle_game(self):
        self.clean_screen("Quorlde Solver")
        for vertical in range(2):
            for horizontal in range(2):
                self.make_game_frame(horizontal, vertical)

    def make_game_frame(self, horizontal, vertical):
        self.frame.append(ttk.Frame(self.window,
                                    borderwidth = 5,
                                    relief = tk.GROOVE))
        self.frame[len(self.game)].grid(column = horizontal, row = vertical)
        self.game.append(Game_Space(self.frame[len(self.game)]))

class Game_Space(object):
    def __init__(self, frame):
        self.frame = frame
        self.game = Wordle()
        self.guess_entry = ttk.Entry(master = self.frame,
                                     width = 11)
        self.buttons_frame = ttk.Frame(master = self.frame)
        self.solve_button = ttk.Button(master = self.frame,
                                       text = "Solve",
                                       command = self.solve_button)
        self.answer_box = tk.Text(master = self.frame,
                                  wrap = tk.NONE,
                                  width = 20,
                                  height = 2)
        self.guess_entry.pack()
        self.buttons_frame.pack()
        self.solve_button.pack()
        self.answer_box.pack()

        self.position_button = []
        for position in range(5):
            def button_action(number = position):
                return self.multi_clicker(number)

            self.position_button.append(ttk.Button(master = self.buttons_frame,
                                                   text = "-",
                                                   command = button_action).grid(column=position, row=3))

    def multi_clicker(self, position):
        pass

    def solve_button(self):
        self.game.solve()
        self.answer_box["state"] = tk.NORMAL
        self.answer_box.insert(tk.END, f"Words = {len(self.game)}\n{self.game}")
        self.answer_box["state"] = tk.DISABLED
