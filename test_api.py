import markov
import sys

text_path = sys.argv[1] if len(sys.argv) >= 2 else "join.txt"

print markov.tweet(text_path)
