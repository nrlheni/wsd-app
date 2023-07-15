from collections import Counter
import re
import string
import nltk
import pickle


# def get_most_frequent_words_in_sentences(filename):
#     # Read the text file
#     with open(filename, 'r', encoding='utf8') as file:
#         text = file.read()

#     # Split text into sentences
#     sentences = re.split(r'\.', text)

#     # Initialize a list to store the most frequent word in each sentence
#     most_frequent_words = []

#     # Process each sentence
#     for sentence in sentences:
#         # Remove punctuation and convert text to lowercase
#         sentence = sentence.lower()
#         sentence = ''.join(c for c in sentence if c.isalpha() or c.isspace())

#         # Split the sentence into words
#         words = sentence.split()

#         # Count the occurrences of each word in the sentence
#         word_counts = Counter(words)

#         if word_counts:
#             # Find the most frequent word in the sentence
#             most_frequent_word = max(word_counts, key=word_counts.get)

#             # Add the most frequent word to the list
#             most_frequent_words.append((sentence, most_frequent_word))

#     # Sort the list based on the most frequent word in each sentence
#     most_frequent_words.sort(key=lambda x: x[1])

#     return most_frequent_words


# # Specify the file path of the text file
# filename = 'D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/article.txt'

# # Call the function and get the most frequent word in each sentence
# most_frequent_words = get_most_frequent_words_in_sentences(filename)

# # Print the most frequent word in each sentence
# for sentence, word in most_frequent_words:
#     print(f'Sentence: {sentence.strip()}')
#     print(f'Most Frequent Word: {word}\n')

import nltk
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder


def identify_ambiguous_words(text):
    # Tokenize the text into words
    words = nltk.word_tokenize(text)

    # Create a BigramCollocationFinder
    finder = BigramCollocationFinder.from_words(words)

    # Apply a measure to rank collocations (PMI in this case)
    measure = BigramAssocMeasures.pmi

    # Filter collocations based on frequency and other criteria
    # Adjust the frequency threshold as per your needs
    finder.apply_freq_filter(5)

    # Get the top 10 collocations
    collocations = finder.nbest(measure, 1)

    # Extract potentially ambiguous words from the collocations
    ambiguous_words = set()
    for collocation in collocations:
        word1, word2 = collocation
        ambiguous_words.add(word1.lower())
        ambiguous_words.add(word2.lower())

    return ambiguous_words


def segment_sentences(text):
    result = []
    # Load the Punkt tokenizer
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()

    # Tokenize the text into sentences
    sentences = tokenizer.tokenize(text)
    for sentence in sentences:
        sentence = sentence.replace(
            '-', ' ').translate(str.maketrans('', '', string.punctuation + '“”'))
        result.append(sentence)

    return result

# Example usage:
# text = "Hello, world! How are you today? I hope you're doing well."
# sentences = segment_sentences(text)
# for sentence in sentences:
#     print(sentence)


filename = 'D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/article.txt'
with open(filename, 'r', encoding='utf8') as file:
    text = file.read()
sentences = segment_sentences(text)
print(sentences)
with open('D:/NurulAkhni/NurulAkhni/SKRIPSI/skripsi-editable/program/wsd-app/article-segmentation.txt', 'w') as file:
    for element in sentences:
        print(element, file=file)
        # ambiguous_words = identify_ambiguous_words(element)
        # print("Potentially ambiguous words:", ambiguous_words)
