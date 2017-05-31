from markov import tweet
import sys

try:
    text_path = sys.argv[1]
except IndexError:
    text_path = "join.txt"

print tweet(text_path)
