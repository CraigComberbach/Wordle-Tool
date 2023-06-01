# Guesser Profiling
from guesser import Guesser
import cProfile
import pstats
import re


# test_answers = re.split("\n", open("Allowable Answers.txt").read())
# test_guesses = ["craig"]
# guesser = Guesser(test_answers, test_guesses)
# print("Expecting less then 2 seconds with 5.029389587559485 bits of info for 'craig'")
# profile = cProfile.Profile()
# profile.runcall(guesser.sift_through_guesses)
# ps = pstats.Stats(profile)
# ps.sort_stats('tottime')
# ps.print_stats()

#Run the game
from wordle import Wordle
from game_gui import Game_GUI


game_boi = Game_GUI()
game_boi.ask_which_game()
game_boi.play_game()
