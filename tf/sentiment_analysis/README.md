# Sentiment Analysis

TensorFlow + NLTK + Python

## NLTK

nltk

text data preprocess

[How to Clean Text for Machine Learning with Python](https://machinelearningmastery.com/clean-text-machine-learning-python/)

[Twitter Sentiment Analysis using NLTK, Python][(](https://towardsdatascience.com/twitter-sentiment-analysis-classification-using-nltk-python-fa912578614c))

## Pandas

[Reading and Writing CSV Files in Python](https://realpython.com/python-csv/#reading-csv-files-with-csv)

[Using iloc, loc, & ix to select rows and columns in Pandas DataFrames](https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/)

## TensorFlow

[TensorFlow Basics: Tensor, Shape, Type, Graph, Sessions & Operators](https://www.guru99.com/tensor-tensorflow.html)

[TensorFlow Architecture](https://github.com/tensorflow/docs/blob/master/site/en/r1/guide/extend/architecture.md)

[TensorFlow best practice series](https://blog.metaflow.fr/tensorflow-how-to-freeze-a-model-and-serve-it-with-a-python-api-d4f3596b3adc)

**Workarounds:**

- Show the graph of saved model,

  ```sh
  saved_model_cli show --dir ./sentiment_model --tag_set serve --all
  ```

- Restore(load) a model

    [Tensorflow: how to save/restore a model?](https://stackoverflow.com/questions/33759623/tensorflow-how-to-save-restore-a-model)

    [Load Saved Model and Predict](https://github.com/AshutoshDongare/Tensorflow-Wide-Deep-Local-Prediction/blob/master/wide_deep_predict.py)

- Restore(load) a model just one time then run(predict) many times efficiently

    [load a TF graph just once, and run it multiple times](https://github.com/tensorflow/tensorflow/issues/19969)

    [How to keep tensorflow session open between predictions? Loading from SavedModel](https://stackoverflow.com/questions/43701902/how-to-keep-tensorflow-session-open-between-predictions-loading-from-savedmodel) ! with block is used for temporary variables and they are destroyed at the block end, so session is destroyed.

- Serve a TensorFlow model with REST/gRPC

    [Serving a model with Flask](https://guillaumegenthial.github.io/serving.html)

    [Deploying Machine Learning Models – pt. 1: Flask and REST API](https://rubikscode.net/2020/02/10/deploying-machine-learning-models-pt-1-flask-and-rest-api/)

    [Creating REST API for TensorFlow models](https://becominghuman.ai/creating-restful-api-to-tensorflow-models-c5c57b692c10)

    [TensorFlow Serving client hosted by Flask web framework](https://github.com/Vetal1977/tf_serving_flask_app) ! Flask + TF Serving

    [Starting a task at startup in Flask](https://networklore.com/start-task-with-flask/)

- Serve a TensorFlow model with TF Serving

    [Tensorflow serving: REST vs gRPC](https://medium.com/@avidaneran/tensorflow-serving-rest-vs-grpc-e8cef9d4ff62)

    [Tensorflow Serving with Docker](https://towardsdatascience.com/tensorflow-serving-with-docker-9b9d87f89f71)

- TensorFlow Project Template

    [Tensorflow-Project-Template](https://github.com/MrGemy95/Tensorflow-Project-Template)

    [Keras-Project-Template](https://github.com/Ahmkel/Keras-Project-Template)



[tfserving-python-predict-client](https://github.com/epigramai/tfserving-python-predict-client)

## .NET Core

[How do I get the path of the assembly the code is in?](https://stackoverflow.com/questions/52797/how-do-i-get-the-path-of-the-assembly-the-code-is-in) !`Environment.CurrentDirectory` has different behaviours when running in visual studio and running by `dotnet run`
