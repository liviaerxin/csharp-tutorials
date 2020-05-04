using System;

namespace RunPythonModule
{
    public class TestAssembly
    {
        static void Main()
        {

            try
            {
                System.Reflection.AssemblyName testAssembly =
                    System.Reflection.AssemblyName.GetAssemblyName(@"/Users/siyao/Documents/csharp-tutorials/pythonnet/src/runtime/bin/netstandard2.0/Python.Runtime.dll");

                System.Console.WriteLine("Yes, the file is an assembly.");
            }

            catch (System.IO.FileNotFoundException)
            {
                System.Console.WriteLine("The file cannot be found.");
            }

            catch (System.BadImageFormatException)
            {
                System.Console.WriteLine("The file is not an assembly.");
            }

            catch (System.IO.FileLoadException)
            {
                System.Console.WriteLine("The assembly has already been loaded.");
            }
        }
    }
}
