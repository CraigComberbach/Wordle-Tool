import math
import re
from wordle import Wordle
from operator import itemgetter


class Guesser(object):
    def __init__(self, answers, guesses):
        self.guesses = guesses
        self.answers = answers
        self.denominator = len(self.answers)

    def sift_through_guesses(self):
        guess_type = ["Known", "Good", "Bad"]
        best_word = []
        best_information = 0

        for index, test_word in enumerate(self.guesses):
            probability = []
            for position1 in guess_type:
                for position2 in guess_type:
                    for position3 in guess_type:
                        for position4 in guess_type:
                            for position5 in guess_type:
                                test_postions = [position1, position2, position3, position4, position5]
                                probability.append(self.probability_of_guess(test_postions, test_word))
            bits_o_info = self.calculate_information(probability)
            best_word.append({"Word":test_word, "Info":bits_o_info})

        best_word = sorted(best_word, key = itemgetter("Info"), reverse = True)
        best_word_list = ""
        for index, word in enumerate(reversed(best_word)):
            print(f"{word['Word']}\t{word['Info']}")
        print("\n")

        for index in range(5):
            if index < len(best_word):
                best_word_list += f"{best_word[index]['Word']} "
        return best_word_list

    def probability_of_guess(self, positions, word):
        model_game = self.create_and_initialize_game()

        for position, state in enumerate(positions):
            if state == "Known":
                model_game.add_known_letters({position: word[position]})
            elif state == "Good":
                model_game.add_good_letters({position: [word[position]]})
            else:
                model_game.add_bad_letters(word[position])
        model_game.solve_answers()
        return len(model_game) / self.denominator

    def create_and_initialize_game(self):
        game = Wordle()
        game.load_default_word_lists()

        return game
    
    def calculate_information(self, probability_array):
        bits_of_information = 0
        for probability in probability_array:
            if probability == 0:
                continue
            bits_of_information += probability * math.log2(probability)
        
        return -bits_of_information