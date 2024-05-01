import nltk
from nltk.stem import PorterStemmer
from collections import defaultdict

# Example list of words
words = ['brace', 'bracing', 'braces', 'braced', 'bracelet', 'bracelets', 'braceletted', 'braceletting', 'braceletted', 'braceletting', 'braceletted', 'braceletting']

# Initialize the stemmer
stemmer = PorterStemmer()

# Stem the words
stemmed_words = [stemmer.stem(word) for word in words]

# Group words by their stem
word_groups = defaultdict(list)
for word, stem in zip(words, stemmed_words):
    word_groups[stem].append(word)

# Print words grouped by their stem
for stem, words in word_groups.items():
    print(f"Stem: {stem}, Words: {words}")
