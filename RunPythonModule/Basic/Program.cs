using System;
using System.Collections.Generic;
using Python.Runtime;

namespace BasicOperation
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine($"CurrentDirectory: {AppDomain.CurrentDomain.BaseDirectory}");

            using (Py.GIL())
            {
                dynamic sys = Py.Import("sys");
                Console.WriteLine($"python version: {sys.version}, sys.path: {sys.path}");

                dynamic os = Py.Import("os");
                Console.WriteLine($"python working directory: {os.getcwd()}");

                // Resolve `calculator.py` not found
                sys.path.insert(0, AppDomain.CurrentDomain.BaseDirectory);

                // Import local module in current directory
                dynamic calculator = Py.Import("calculator");
                Console.WriteLine($"import calculator module");

                Console.WriteLine($"run function:");
                Console.WriteLine($"5 + 10 = {calculator.add(5, 10)}");

                Console.WriteLine($"run class:");
                Console.WriteLine($"5 + 10 = {calculator.Calculator().add(5, 10)}");

                Console.ReadKey();
            }
        }
    }
}
