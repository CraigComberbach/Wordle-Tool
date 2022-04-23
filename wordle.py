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
        self.word_list = re.split("\n", open("Allowable Answers.txt").read())

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

    def must_have_letter_at_specific_location(self):
        for index in reversed(range(0, len(self.word_list))):
            for position, letter in self.known_letters.items():
                pattern = self.make_five_letter_pattern_string(letter, position)
                if re.search(pattern, self.word_list[index]) is None:
                    self.word_list.remove(self.word_list[index])
                    break

    def only_include_valid_letters(self):
        for position, letter_list in self.good_letters.items():
            for letter in letter_list:
                for index in reversed(range(0, len(self.word_list))):
                    pattern = self.make_five_letter_pattern_string(letter, position)

                    # Remove word if the valid letter doesn't exist in the word at all or exists in an invalid location
                    if re.search(letter, self.word_list[index]) is None \
                        or re.search(pattern, self.word_list[index]) is not None \
                        and pattern != ".....":
                        self.word_list.remove(self.word_list[index])

    def remove_invalid_letters(self):
        for index in reversed(range(0, len(self.word_list))):
            for letter in self.bad_letters:
                if re.search(letter, self.word_list[index]) is not None:
                    self.word_list.remove(self.word_list[index])
                    break

    def make_five_letter_pattern_string(self, letter, index):
        pattern_string = ""
        for position in range(index):
            pattern_string += "."
        pattern_string += letter
        for position in range(5 - len(pattern_string)):
            pattern_string += "."
        return pattern_string

    def solve(self):
        self.must_have_letter_at_specific_location()
        self.only_include_valid_letters()
        self.remove_invalid_letters()

    def __str__(self):
        return f"{self.word_list}"

    def __len__(self):
        return len(self.word_list)
