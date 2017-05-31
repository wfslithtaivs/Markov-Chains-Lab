"""Generate markov text from text files.

    to run from command line:
    python markov.py gettysburg.txt
"""


from random import choice
import re
import sys

# get n-gram size from command line input

MAX_GRAM_SIZE = 5


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    # your code goes here

    f = open(file_path)

    return f.read()


def produce_n_gram_dict(text_corpus):
    """Produce dictionary of n-grams"""

    n_dict = {}

    for char in text_corpus:
        if char in ["(", ")", "\"", "\'", "\'", "`", "_", "*", "__", "--", "[", "]"]:
            text_corpus.replace(char,'')

    text_corpus = text_corpus.split()

    for n in range(2, MAX_GRAM_SIZE + 1):
        for i in range(len(text_corpus) - n):
            current_n_words = tuple(text_corpus[i:i+n])

            next_word = [text_corpus[i + n]]

            if n_dict.get(current_n_words) is None:
                n_dict[current_n_words] = next_word
            else:
                n_dict[current_n_words] += next_word

    return n_dict

def generate_tweet(dictionary):
    """Generate random 140 chars tweet"""

    while True:
        current_seed = choice(dictionary.keys())
        if len(current_seed) >= 3:
            break

    window_limit = len(current_seed)
    window_size = window_limit

    message = []
    message.extend(current_seed)
    message[0] = message[0].capitalize()

    while True:
        if window_size == 1:
            break

        current_n_gram = tuple(message[-1*window_size:])

        try:
            next_word = choice(dictionary[current_n_gram])
            if (len(" ".join(message)) + len(next_word) + 2) > 140:
                return output_message(message)
            else:
                message.append(next_word)
                window_size = window_limit
        except KeyError:
            window_size -= 1
            continue

    return output_message(message)


def output_message(message_list):
    """Produce meaningful ending for message"""

    result = " ".join(message_list)

    if result[-1] in ["!", "?", "."]:
        return result
    elif result[-1] in [",", "-", " ", ":", ";"]:
        return result[:-1] + "."
    elif result[-2:] is "--":
        return result[:-2] + "."
    else:
        return result + "."


def tweet(file_name = "green-eggs.txt"):
    """Generate tweet from given text file """

    input_text = open_and_read_file(file_name)
    n_grams = produce_n_gram_dict(input_text)
    return generate_tweet(n_grams)
