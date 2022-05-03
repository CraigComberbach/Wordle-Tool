import math
import re
from wordle import Wordle

class Guesser(object):
    def __init__(self, answers, guesses):
        self.guesses = guesses
        self.answers = answers
        self.denominator = len(self.answers)

    def sift_through_guesses(self):
        guess_type = ["Known", "Good", "Bad"]
        for test_word in self.guesses:
            probability = []
            for position1 in guess_type:
                for position2 in guess_type:
                    for position3 in guess_type:
                        for position4 in guess_type:
                            for position5 in guess_type:
                                test_postions = [position1, position2, position3, position4, position5]
                                probability.append(self.probability_of_guess(test_postions, test_word))
            bits_o_info = self.calculate_information(probability)
            print(f"{test_word} has {bits_o_info} bits of information")

    def probability_of_guess(self, positions, word):
        model_game = self.create_and_initialize_game()

        for position, state in enumerate(positions):
            if state == "Known":
                model_game.add_known_letters({position: word[position]})
            elif state == "Good":
                model_game.add_good_letters({position: [word[position]]})
            else:
                model_game.add_bad_letters(word[position])
        model_game.solve()
        return len(model_game) / self.denominator

    def create_and_initialize_game(self):
        game = Wordle()
        game.word_list = []
        for word in self.answers:
            game.word_list.append(word)
        return game
    
    def calculate_information(self, probability_array):
        bits_of_information = 0
        for probability in probability_array:
            if probability == 0:
                continue
            bits_of_information += probability * math.log2(probability)
        
        return -bits_of_information