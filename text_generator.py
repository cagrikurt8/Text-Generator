from nltk.tokenize import regexp_tokenize
from collections import Counter
from random import choices

file_path = "corpus.txt"
corpus = open(file_path, 'r', encoding="utf-8")


def welcome():
    print("Welcome! This is a sentence-generator program based on Game of Thrones scenario."
          "\nHere are options for you to make:"
          "\n\n1. Get statistics of the scenario(numbers of words, two-word phrases and three-word phrases)"
          "\n2. Get words, bigrams or trigrams by index"
          "\n3. Get 5 top possible combinations of two words(bigram) and their number of occurrences by entering a word"
          "\n4. Generate some random texts."
          "\n5. Generate meaningful sentences.")


class NLPObject:

    token_list = list()
    bigram_list = list()
    ht_count_dict = dict()
    trigram_list = list()
    htt_count_dict = dict()

    def __init__(self, token):
        self.token_list = token
        self.bigram_list = [[self.token_list[x], self.token_list[x+1]] for x in range(len(self.token_list) - 1)]
        for element in self.bigram_list:
            self.ht_count_dict.setdefault(element[0], list()).append(element[1])
        self.trigram_list = [[self.token_list[x] + " " + self.token_list[x+1], self.token_list[x+2]] for x in range(len(self.token_list) - 2)]
        for member in self.trigram_list:
            self.htt_count_dict.setdefault(member[0], list()).append(member[1])

    def get_bigram_list(self):
        return self.bigram_list

    def get_trigram_list(self):
        return self.trigram_list

    def get_statistics(self):
        print("Corpus statistics")
        print(f"All tokens: {len(self.token_list)}")
        print(f"Unique tokens: {len(set(self.token_list))}")
        print()
        print(f"Number of bigrams: {len(self.bigram_list)}")
        print()
        print(f"Number of trigrams: {len(self.trigram_list)}")

    def get_value_by_index(self, value):
        while True:

            idx = input("Index: ")
            if idx == "exit":
                break
            else:
                try:
                    int(idx)
                except ValueError:
                    print("Type Error. Please input an integer.")
                else:
                    if value == "tokens":
                        try:
                            self.token_list[int(idx)]
                        except IndexError:
                            print("Index Error. Please input an integer that is in the range of the corpus.")
                        else:
                            print(f"{self.token_list[int(idx)]}")
                    elif value == "bigrams":
                        try:
                            self.bigram_list[int(idx)]
                        except IndexError:
                            print("Index Error. Please input a value that is not greater than the number of all bigrams.")
                        else:
                            print(f"Head: {self.bigram_list[int(idx)][0]}    Tail: {self.bigram_list[int(idx)][1]}")
                    elif value == "trigrams":
                        try:
                            self.trigram_list[int(idx)]
                        except IndexError:
                            print("Index Error. Please input a value that is not greater than the number of all trigrams.")
                        else:
                            print(f"Head: {self.trigram_list[int(idx)][0]}  Tail: {self.trigram_list[int(idx)][1]}")

    def count_ht(self):
        while True:
            word = input("Word: ")
            if word == "exit":
                break
            try:
                tails = Counter(self.ht_count_dict[word]).most_common()
            except KeyError:
                print("The requested word is not in the model. Please input another word.")
            else:
                print(f"Head: {word}")
                counter = 0
                for a, b in tails:
                    print(f"Tail: {a}   Count: {b}")
                    counter += 1
                    if counter >= 5:
                        break

    def generate_random_text(self):
        word = choices(self.token_list)[0]
        sentence = f"{word}"
        while len(sentence.split()) < 10:
            tail_list = Counter(self.ht_count_dict[word]).most_common()
            prob_word_list = [x[0] for x in tail_list]
            freq_list = [x[1] for x in tail_list]
            following_word = choices(prob_word_list, freq_list)[0]
            sentence = sentence + " " + following_word
            word = following_word
        print(sentence)

    def generate_full_sentences(self):
        sentence = str()
        while True:
            head = choices(self.trigram_list)[0][0]
            control = head.split()
            if head[0].isupper() and "." not in control[0] and "?" not in control[0] and "!" not in control[0]:
                sentence = sentence + " " + head
                break
        condition = True
        while condition:
            x = sentence.split()[-2] + " " + sentence.split()[-1]
            for tkn in self.trigram_list:
                if x in tkn:
                    sentence = sentence + " " + tkn[1]
                    if (sentence.endswith(".") or sentence.endswith("?") or sentence.endswith("!")) and len(sentence.split()) >= 5:
                        condition = False
                    break
        print(sentence)


model_object = NLPObject(regexp_tokenize(corpus.read(), r"\S+"))
cnd = True
welcome()
while cnd:
    chc = input("\nEnter 'exit' if you want to exit"
                "\n>")

    if chc == "exit":
        cnd = False

    elif chc == "1" or chc == "1.":
        model_object.get_statistics()

    elif chc == "2" or chc == "2.":
        model_object.get_value_by_index(input("Enter 'tokens' for single words, 'bigrams' for two-word phrases, 'trigrams' for three-word phrases."
                                              "\n>"))
    elif chc == "3" or chc == "3.":
        model_object.count_ht()

    elif chc == "4" or chc == "4.":
        for i in range(10):
            model_object.generate_random_text()
    elif chc == "5" or chc == "5.":
        for i in range(10):
            model_object.generate_full_sentences()
