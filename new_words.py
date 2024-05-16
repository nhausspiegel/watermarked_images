# easy fake word generator!
# takes a set of morphemes and generates new words by pairing up random prefixes and suffixes.
# some of the words will be real. that's fine.

# morphemes.json accessed from https://github.com/colingoldberg/morphemes

import json
import random

f = open("morphemes.json")
morphemes = json.load(f)

# get all prefixes
prefixes = []
for m in morphemes:
    for form in morphemes[m]["forms"]:
        if form["loc"] == "prefix":
            prefixes.append(form["form"])

# get all suffixes
suffixes = []
for m in morphemes:
    for form in morphemes[m]["forms"]:
        if form["loc"] == "suffix":
            suffixes.append(form["form"])

# easy way to shuffle these lists
prefixes = list(set(prefixes))
suffixes = list(set(suffixes))

# generate all possible combinations
new_words = []
for prefix in prefixes:
    for suffix in suffixes:
        new_words.append((prefix + suffix).lower())

words_file = open("words.txt", "w")
random.shuffle(new_words)
for word in new_words:
    words_file.write(word + "\n")
words_file.close()
