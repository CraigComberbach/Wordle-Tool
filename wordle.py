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
        for position, letter in letter_dictionary.items():
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

                    # Remove word if the valid letter doesn't exist in the word at all
                    if re.search(letter, self.word_list[index]) is None:
                        self.word_list.remove(self.word_list[index])
                    # Remove word if the valid letter exists in an invalid location
                    elif re.search(pattern, self.word_list[index]) is not None and pattern != ".....":
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
        # print(f"Initial Word List ({len(self.word_list)})\t{self.word_list}")
        self.must_have_letter_at_specific_location()
        # print(f"Known Letters Only ({len(self.word_list)})\t{self.word_list}")
        self.only_include_valid_letters()
        # print(f"Valid Letters Only ({len(self.word_list)})\t\t{self.word_list}")
        self.remove_invalid_letters()
        # print(f"Remove Invalid Letters ({len(self.word_list)})\t{self.word_list}")

    def __str__(self):
        return f"{len(self.word_list):4d} - {self.word_list}"