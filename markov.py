"""Generate markov text from text files."""


from random import choice
import re
import sys


def open_and_read_file(file_path):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    # your code goes here

    f = open(file_path)

    return f.read()


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
    """

    chains = {}

    # your code goes here
    # could also be done with word.corpus.split(), but this would require
    # special handling at the end of the list
    word_corpus = re.split(' |\n', text_string)

    # iterate over word corpus
    for i, word in enumerate(word_corpus):
        # if we hit the end of meaningful pairs - break
        if word_corpus[i + 1] == "":
            break
        # otherwise, we still have valid pairs to check/add
        else:
            current_pair = (word, word_corpus[i + 1])
            # checks if current pair already exists in dictionary
            existing_values = chains.get(current_pair)
            # if get fn returns None, current pair does not exist yet
            if existing_values == None:
                # add current pair as a key and add next word as a list
                chains[current_pair] = [word_corpus[i + 2]]
            # otherwise, current pair already exists in dictionary
            else:
                # add new word to existing list so as to not overwrite values
                chains[current_pair] += [word_corpus[i + 2]]

    return chains


def make_text(chains):
    """Returns text from chains."""

    words = []

    # your code goes here
    # choose random pair from dictionary keys (bigram tuples)
    random_pair = choice(chains.keys())
    # change tuple to a list and append to words list
    words.extend(random_pair)
    # grab a random next word from the key's values list
    next_word = choice(chains[random_pair])
    # repeat until word pair not in dictionary - indicates end of text
    words.append(next_word)

    while True:
        # create new tuple from last two words of word chain
        new_pair = tuple(words[-2:])
        # attempt to get next word, break if not available
        try:
            new_next_word = choice(chains[new_pair])
        except KeyError:
            break
        # if here, new next word found, append to words
        words.append(new_next_word)
    # for aesthetics, capitalize first word
    words[0] = words[0].capitalize()
    # join words list into a string and return
    return " ".join(words)

try:
    input_path = sys.argv[1]
except IndexError:
    input_path = "green-eggs.txt"
    print "Using default text file."


# Open the file and turn it into one long string
input_text = open_and_read_file(input_path)

# Get a Markov chain
chains = make_chains(input_text)

# for item, value in chains.items():
#     print item, "-", value

# Produce random text
random_text = make_text(chains)

#print random_text

# try a list comprehension
texts = [make_text(chains) for i in range(25)]

for text in texts:
    print text
    print
