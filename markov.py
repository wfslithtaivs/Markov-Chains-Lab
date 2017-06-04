"""Generate markov text from text files.

    to run from command line:
    python markov.py gettysburg.txt
"""

import os
import choice
import re
import sys
import twitter


# get n-gram size from command line input

MAX_GRAM_SIZE = 5


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    with open(file_path, 'r') as f:
        return f.read()

def produce_n_gram_dict(text_corpus):
    """Produce dictionary of n-grams"""

    for ch in ["(", ")", "\"", "\'", "\'", "`", "_", "*", "__", "--", "[", "]"]:
        text_corpus = text_corpus.replace(ch, '')

    text_corpus = text_corpus.split()

    n_dict = {}
    for n in range(2, MAX_GRAM_SIZE + 1):
        for i in range(len(text_corpus) - n):
            current_n_words = tuple(text_corpus[i:i+n])
            next_word = text_corpus[i + n]
            n_dict.setdefault(current_n_words, []).append(next_word)

    return n_dict


def generate_tweet(n_dict):
    """Generate random 140 chars tweet"""

    while True:
        current_seed = random.choice(n_dict.keys())
        if len(current_seed) >= 3:
            break

    window_limit = len(current_seed)
    window_size = window_limit

    message = list(current_seed)
    message[0] = message[0].capitalize()

    while window_size > 1:
        current_n_gram = tuple(message[-window_size:])

        if current_n_gram in n_dict:
            next_word = random.choice(n_dict[current_n_gram])
            if len(" ".join(message)) + len(next_word) + 12 > 140:
                break

            message.append(next_word)
            window_size = window_limit
        else:
            window_size -= 1

    return output_message(message)


def output_message(message_list):
    """Produce meaningful ending for message"""

    result = " ".join(message_list)

    if result[-1:] in [",", "-", " ", ":", ";"]:
        result = result[:-1] + "."
    elif result[-2:] == "--":
        result = result[:-2] + "."
    elif result[-1:] not in ["!", "?", "."]:
        result += "."

    return result + " #aug17kat"


def tweet(file_name = "green-eggs.txt"):
    """Generate tweet from given text file """

    input_text = open_and_read_file(file_name)
    n_grams = produce_n_gram_dict(input_text)

    api = twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    twt = generate_tweet(n_grams)
    status = api.PostUpdate(twt)
    return twt


if __name__ == '__main__':
    text_path = sys.argv[1] if len(sys.argv) >= 2 else "join.txt"
    print tweet(text_path)

# #aug17kat
