using System;
using System.Collections.Generic;
using Python.Runtime;
using System.Diagnostics;

namespace TensorFlow
{
    class Program
    {
        static readonly List<string> listOfReviewText = new List<string>()
        {
            "this film is really good",
            "this film is really bad",
            "this film is really normal",
            "My favorite movie of all time",
            "This is How Movie Should Be Made",
            "There's just no point anymore",
            "Awful, pure stupidity",
            "You don't need  to see it"
        };

        static void Main(string[] args)
        {
            using (Py.GIL())
            {
                Console.WriteLine("Using Python Runtime to run TensorFlow");

                dynamic tf = Py.Import("tensorflow");
                Console.WriteLine($"tf version: {tf.__version__}");

                dynamic sys = Py.Import("sys");
                //Resolve `sentiment analysis module` not found
                sys.path.insert(0, AppDomain.CurrentDomain.BaseDirectory);

                //Import local module in current directory
                Console.WriteLine($"Importing sentiment analysis module...");


                dynamic analysis = Py.Import("sentiment_analysis.sentiment_analysis");

                // Predict without keeping context
                //foreach (var text in listOfReviewText)
                //{
                //    // Run prediction
                //    dynamic result = null;
                //    var elapsedTime = Profile(() => result = analysis.predict(text));

                //    Console.WriteLine($"ReviewText: {text}");
                //    Console.WriteLine($"Is sentiment/review positive?: {result[0]}");
                //    Console.WriteLine($"Prediction Confidence: {result[1]}");

                //    Console.WriteLine($"consuming time: {elapsedTime}ms");
                //}

                // Predict with keeping contextsentiment_analysis.sentiment_analysis
                dynamic model = analysis.Model();

                foreach (var text in listOfReviewText)
                {
                    // Run prediction
                    dynamic result = null;
                    var elapsedTime = Profile(() => result = model.predict(text));

                    Console.WriteLine($"ReviewText: {text}");
                    Console.WriteLine($"Is sentiment/review positive?: {result[0]}");
                    Console.WriteLine($"Prediction Confidence: {result[1]}");

                    Console.WriteLine($"consuming time: {elapsedTime}ms");
                }

            }
        }

        static long Profile(Action method)
        {
            Stopwatch st = Stopwatch.StartNew();
            method();
            st.Stop();
            return st.ElapsedMilliseconds;
        }
    }
}
