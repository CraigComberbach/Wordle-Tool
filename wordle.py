import re

class Wordle(object):
    def __init__(self):
        self.bad_letters = []
        self.good_letters = {0: [],
                             1: [],
                             2: [],
                             3: [],
                             4: []}
        self.known_letters = {0: "",
                              1: "",
                              2: "",
                              3: "",
                              4: ""}
        self.answer_list = []
        self.guess_list = []

    def load_default_word_lists(self):
        self.answer_list = re.split("\n", open("Allowable Answers.txt").read())
        self.guess_list = re.split("\n", open("Modified Allowable Guesses.txt").read())

    def add_bad_letters(self, letters):
        for letter in list(letters):
            self.bad_letters.append(letter)

    def add_good_letters(self, letter_dictionary):
        for position, letters in letter_dictionary.items():
            for letter in letters:
                self.good_letters[position].append(letter)

    def add_known_letters(self, letter_dictionary):
        for position, letter in letter_dictionary.items():
            self.known_letters[position] = letter

    def any_letter_match(self, pattern_letter, word):
        for letter in word:
            if pattern_letter == letter:
                return True
        return False

    def letter_at_specific_position_match(self, pattern_letter, position, word):
        if pattern_letter == word[position]:
            return True
        else:
            return False

    def must_have_letter_at_specific_location(self, word_list):
        for index in reversed(range(0, len(word_list))):
            for position, letter in self.known_letters.items():
                if letter == "":
                    continue
                if self.letter_at_specific_position_match(letter, position, word_list[index]) == False:
                    word_list.pop(index)
                    break

    def only_include_valid_letters(self, word_list):
        for position, letter_list in self.good_letters.items():
            for letter in letter_list:
                if letter == "":
                    continue
                for index in reversed(range(0, len(word_list))):
                    # Remove word if the valid letter doesn't exist in the word at all or exists in an invalid location
                    if self.any_letter_match(letter, word_list[index]) == False \
                            or self.letter_at_specific_position_match(letter, position, word_list[index]) == True:
                        word_list.pop(index)

    def remove_invalid_letters(self, word_list):
        for index in reversed(range(0, len(word_list))):
            for letter in self.bad_letters:
                if self.any_letter_match(letter, word_list[index]) == True:
                    word_list.pop(index)
                    break

    def ensure_letter_integrity(self):
        # Reduce bad letters to only have unique letter to reduce redundancy
        self.bad_letters = list(set(self.bad_letters))

        # I am putting a greater weight on a good/known letter over a bad letter
        # The online game will mark a repeated good letter as a bad letter
        # eg woods will mark the first 'o' as good and the second 'o' as bad
        for position, letters in self.good_letters.items():
            for letter in letters:
                if letter in self.bad_letters:
                    self.bad_letters.remove(letter)

        for position, letter in self.known_letters.items():
            if letter in self.bad_letters:
                self.bad_letters.remove(letter)

    def solve(self):
        self.solve_answers()
        self.solve_guesses()

    def solve_answers(self):
        self.ensure_letter_integrity()
        self.remove_invalid_letters(self.answer_list)
        self.only_include_valid_letters(self.answer_list)
        self.must_have_letter_at_specific_location(self.answer_list)

    def solve_guesses(self):
        self.ensure_letter_integrity()
        self.remove_invalid_letters(self.guess_list)
        self.only_include_valid_letters(self.guess_list)
        self.must_have_letter_at_specific_location(self.guess_list)

    def __str__(self):
        list_of_answers = ""
        for word in self.answer_list:
            list_of_answers += f"{word}, "
        return list_of_answers

    def __len__(self):
        return len(self.answer_list)
