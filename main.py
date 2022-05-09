from wordle import Wordle
from game_gui import Game_GUI
from guesser import Guesser

game_boi = Game_GUI()
game_boi.ask_which_game()
game_boi.play_game()

# # Guesser Profiling
# import cProfile
# import pstats
# import re
# test_answers = re.split("\n", open("Allowable Answers.txt").read())
# test_guesses = ["craig"]
# guesser = Guesser(test_answers, test_guesses)
# print("Expecting less then 7 seconds")
# profile = cProfile.Profile()
# profile.runcall(guesser.sift_through_guesses)
# ps = pstats.Stats(profile)
# ps.sort_stats('tottime')
# ps.print_stats()
