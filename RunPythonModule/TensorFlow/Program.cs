using System;
using System.Collections.Generic;
using Python.Runtime;

namespace TensorFlow
{
    class Program
    {
        static void Main(string[] args)
        {
            using(Py.GIL())
            {
                Console.WriteLine("Using Python Runtime");

                dynamic tf = Py.Import("tensorflow");
                Console.WriteLine($"tf version: {tf.__version__}");

            }
        }
    }
}
