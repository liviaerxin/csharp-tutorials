#!/usr/bin/env python3

import os
import re
import time
import functools

import numpy as np
import pandas
import tensorflow as tf  # tf version 1.15
from keras import preprocessing
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from tensorflow import keras
from textblob import TextBlob

dir_path = os.path.dirname(os.path.realpath(__file__))
model_dir = os.path.join(dir_path, "./sentiment_model")

signature_key = tf.saved_model.DEFAULT_SERVING_SIGNATURE_DEF_KEY
input_key = "Features"
output_key = "Prediction"

df = pandas.read_csv(
    os.path.join(model_dir, "imdb_word_index.csv"),
    index_col="word",
    header=0,
    names=["word", "id"],
)


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value

    return wrapper_timer


# Removal of punctuations.
def form_sentence(tweet):
    tweet_blob = TextBlob(tweet)
    return " ".join(tweet_blob.words)


lemmatizer = WordNetLemmatizer()
lemmatizer.lemmatize("test")  # initialize


def preprocess(text: str):
    # 1. Remove non-letters
    words = form_sentence(text)

    # 2. Split into individual words
    words = word_tokenize(words.lower())

    # 3. Remove stop words
    meaningful_words = [w for w in words if not w in stopwords.words("english")]

    # 4. Stem words
    words = [lemmatizer.lemmatize(w, "v") for w in meaningful_words]

    # df = pandas.read_csv(
    #     os.path.join(model_dir, "imdb_word_index.csv"),
    #     index_col="word",
    #     header=0,
    #     names=["word", "id"],
    # )

    # 5. Index words
    indexed_words = []

    for word in words:
        if word in df.index:
            index = df.loc[word]["id"]
        else:
            index = 0
        indexed_words.append(index)

    # print(indexed_words)

    # 6. Pad indexes
    indexed_words = preprocessing.sequence.pad_sequences(
        [indexed_words], padding="post", truncating="post", maxlen=600, dtype="int32"
    )

    return indexed_words


def predict(text: str):
    """predict on a new session. Once session has closed, all context in it will be destroyed.

    Arguments:
        text {str} -- [description]

    Returns:
        [type] -- [description]
    """
    with tf.Session(graph=tf.Graph()) as sess:
        print("\nPredicting...")
        # load the saved model
        print(f"Restoring saved model: {model_dir}")

        meta_graph_def = tf.saved_model.loader.load(sess, ["serve"], model_dir)

        signature = meta_graph_def.signature_def

        x_tensor_name = signature[signature_key].inputs[input_key].name
        y_tensor_name = signature[signature_key].outputs[output_key].name

        x = sess.graph.get_tensor_by_name(x_tensor_name)
        y = sess.graph.get_tensor_by_name(y_tensor_name)

        print(f"input tensor: {x}, \noutput tensor: {y}")

        # text = "this film is really good"

        data = preprocess(text)

        start = time.time()
        y_out = sess.run(y, feed_dict={x: data})
        print(f"session running time: {time.time() - start}")

        y_out = y_out.reshape(-1)
        positive = "Yes" if y_out[1] > 0.5 else "No"
        confidence = y_out[1] if y_out[1] > 0.5 else y_out[0]

        # print(f"Number of classes: {y_out.shape[0]}")
        # print(f"Is sentiment/review positive?: {p}")
        # print(f"Prediction Confidence: {c}")

        return positive, confidence
        # graph = tf.get_default_graph()
        # for op in graph.get_operations():
        #     print(op.name, op.outputs)

        # Get restored placeholders
        # labels_data_ph = graph.get_tensor_by_name('labels_data_ph:0')
        # features_data_ph = graph.get_tensor_by_name('features_data_ph:0')
        # batch_size_ph = graph.get_tensor_by_name('batch_size_ph:0')
        # # Get restored model output
        # restored_logits = graph.get_tensor_by_name('dense/BiasAdd:0')
        # # Get dataset initializing operation
        # dataset_init_op = graph.get_operation_by_name('dataset_init')

        # get the predictor , refer tf.contrib.predictor
        # predictor = tf.contrib.predictor.from_saved_model(model_dir)

        # print(predictor)


class Model(object):
    """A model class used to persist the session holding the graph context for multiple times of predictions

    Arguments:
        object {[type]} -- [description]
    """

    def __init__(self, saved_model: str = model_dir):
        self.saved_model = saved_model

        self._load_model(saved_model)

    def _load_model(self, saved_model):
        # load the saved model
        print(f"Restoring saved model: {saved_model}")

        self.sess = tf.Session(graph=tf.Graph())
        self.meta_graph_def = tf.saved_model.loader.load(
            self.sess, [tf.saved_model.tag_constants.SERVING], saved_model
        )

        signature = self.meta_graph_def.signature_def

        input_tensor_name = signature[signature_key].inputs[input_key].name
        output_tensor_name = signature[signature_key].outputs[output_key].name

        self.input_tensor = self.sess.graph.get_tensor_by_name(input_tensor_name)
        self.output_tensor = self.sess.graph.get_tensor_by_name(output_tensor_name)

    def predict(self, text: str):
        print("\nPredicting...")

        # text = "this film is really good"
        data = preprocess(text)

        start = time.time()
        output = self.sess.run(
            self.output_tensor, feed_dict={self.input_tensor: data}
        )  # sess.run slower in first time
        print(f"session running time: {time.time() - start}")

        output = output.reshape(-1)
        positive = "Yes" if output[1] > 0.5 else "No"
        confidence = output[1] if output[1] > 0.5 else output[0]

        # print(f"Number of classes: {y_out.shape[0]}")
        # print(f"Is sentiment/review positive?: {p}")
        # print(f"Prediction Confidence: {c}")

        return str(positive), float(confidence)


if __name__ == "__main__":
    model = Model()
    p, c = model.predict("This film is really good. Not bad.")
    print(f"Is sentiment/review positive?: {p}")
    print(f"Prediction Confidence: {c}")
