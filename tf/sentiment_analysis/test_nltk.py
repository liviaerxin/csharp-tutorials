#!/usr/bin/env python3

import csv
import re
import ssl
import string

import nltk
import pandas
from keras import preprocessing
from keras.datasets import imdb
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from textblob import TextBlob

text = "It isn't good. Some modeling tasks prefer input to be in the form of paragraphs or sentences, such as word2vec. You could first split your text into sentences, split each sentence into words, then save each sentence to file, one per line."

sentence = """At eight o'clock on Thursday morning
... Arthur didn't feel very good."""

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


word2index = imdb.get_word_index()

test = []

for word in nltk.word_tokenize("i love this movie"):
    print(word)
    test.append(word2index[word])

test = preprocessing.sequence.pad_sequences([test], maxlen=10)

print(test)

# Removal of punctuations.
def form_sentence(tweet):
    tweet_blob = TextBlob(tweet)
    return " ".join(tweet_blob.words)


# Removal of commonly used words (stopwords).
def no_user_alpha(tweet):
    tweet_list = [ele for ele in tweet.split() if ele != "user"]
    clean_tokens = [t for t in tweet_list if re.match(r"[^\W\d]*$", t)]
    clean_s = " ".join(clean_tokens)
    clean_mess = [
        word
        for word in clean_s.split()
        if word.lower() not in stopwords.words("english")
    ]
    return clean_mess


# Normalization of words.
def normalization(tweet_list):
    lem = WordNetLemmatizer()
    normalized_tweet = []
    for word in tweet_list:
        normalized_text = lem.lemmatize(word, "v")
        normalized_tweet.append(normalized_text)
    return normalized_tweet


# Indexing word
def index(word):
    if word in word2index:
        return word2index[word]
    else:
        return 0


def sequence(text):
    # split into words
    words = nltk.word_tokenize(text)

    # remove all tokens that are not alphabetic
    # words=[word.lower() for word in words if word.isalpha()]

    return words


words = normalization((no_user_alpha(form_sentence(text))))
print(words)

df = pandas.read_csv(
    "./sentiment_model/imdb_word_index.csv",
    index_col="word",
    header=0,
    names=["word", "id"],
)
print(df)

# Index words
indexed_words = []

for word in words:
    if word in df.index:
        index = df.loc[word]["id"]
    else:
        index = 0
    indexed_words.append(index)

print(indexed_words)

# Pad indexed words
indexed_words = preprocessing.sequence.pad_sequences(
    [indexed_words], padding="post", truncating="post", maxlen=600, dtype="int32"
)

print(indexed_words)
