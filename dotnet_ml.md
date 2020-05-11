# .NET for ML(Machine Learning)

For .NET App(Console, Deskop) to interface python ML server(TensorFlow),

1. [ML.NET Documentation](https://docs.microsoft.com/en-us/dotnet/machine-learning/) !Add ML to .NET applications

   Samples:

   - [Run with ML.NET C# code a TensorFlow model exported from Azure Cognitive Services Custom Vision](https://devblogs.microsoft.com/cesardelatorre/run-with-ml-net-c-code-a-tensorflow-model-exported-from-azure-cognitive-services-custom-vision/)
   - [Tutorial: Analyze sentiment of movie reviews using a pre-trained TensorFlow model in ML.NET](https://docs.microsoft.com/en-us/dotnet/machine-learning/tutorials/text-classification-tf)

2. .NET Bindings for TensorFlow.

   Bindings:

   - [SciSharp TensorFlow.NET](https://github.com/SciSharp/TensorFlow.NET) !Python naming convention and broader support for the higher level operations
   - [TensorFlowSharp](https://github.com/migueldeicaza/TensorFlowSharp)

   Samples:

   - [Run TensorFlow Machine Learning Code In C# With Almost No Changes](https://medium.com/machinelearningadvantage/run-tensorflow-machine-learning-code-in-c-with-almost-no-changes-77f7b629389)
   - [TensorFlow - Creating C# Applications using TensorFlowSharp](https://www.codeproject.com/Articles/5164135/TensorFlow-Creating-Csharp-Applications-using)

3. Run Python Script from C#.

   - [Running Python Script From C# and Working With the Results](https://medium.com/better-programming/running-python-script-from-c-and-working-with-the-results-843e68d230e5)
   - [Using C# to run Python Scripts with Machine Learning Models](https://medium.com/@ernest.bonat/using-c-to-run-python-scripts-with-machine-learning-models-a82cff74b027)
   - [Invoking TensorFlow AI (Python) from a C# Desktop Application](https://www.codeproject.com/Articles/5248149/Invoking-TensorFlow-AI-Python-from-a-Csharp-Deskto)

   Seeing project at [RunPythonScript](RunPythonScript/Program.cs)

4. Call Python code as module from C#

   [pythonnet - Python for .NET](https://github.com/pythonnet/pythonnet) !Calling .NET code from Python or Embedding Python in .NET
   [IronPython](https://ironpython.net/) !access to numpy, pandas, ...etc third libs are not well supported!

   Seeing project at [RunPythonModule/TensorFlow](RunPythonModule/TensorFlow/Program.cs)

5. Client/Server Architecture

   Services Components:

   - .NET App(Client)
   - Python REST/gRPC Server(Server)

Available solutions for Client/Server Architecture:

- .NET App and python server would run sperately(two independent processes)

  1. start python server(as a service or daemon, systemd)
  2. start .NET App
  3. create a client in .NET App
  4. interface python server through the created client
  5. exit .NET App
  6. repeat 2 to 5
  7. terminate python server

  for using windows services(Windows),

  1. install windows service application, it holds a python server
  2. start .NET App
  3. start the windows service(start python server) from code in .NET App
  4. create a client in .NET App
  5. interface python server through the created client
  6. stop the windows service(stop python server) from code in .NET App
  7. exit .NET App
  8. repeat 2 to 7
  9. uninstall windows service application

- .NET App would control python server to start/stop(.NET App embed python server)

  1. start .NET App
  2. start python server in .NET App(as a process)
  3. create a client in .NET App
  4. interface python server through the created client
  5. terminate python server in .NET App
  6. exit .NET App
  7. repeat 1 to 6

  for .NET to control python server in step 2 and 5, there are two several implementations:

  - .NET imports python server as module which will run a server in a python thread/process(?)

  gRPC server already contains the feature. However for flask server, it need a server wrapper that can controller the flask server start/stop in a new spawn process.

  grpc problems:

  see the belowing code:

  ```c#
  public static void RunGRPC()
      {
          dynamic server;

          using (Py.GIL())
          {
              Console.WriteLine("ML App Embed Python Server!");

              dynamic sys = Py.Import("sys");
              //Resolve `sentiment analysis module` not found
              sys.path.insert(0, AppDomain.CurrentDomain.BaseDirectory);

              //Import local module in current directory
              Console.WriteLine($"Importing run grpc module...");

              //Start a server
              dynamic grpc_server = Py.Import("sentiment_analysis.grpc_server");

              server = grpc_server.creater_server();

              server.start(); //non blocking
              Console.WriteLine($"gRPC server starting...");

          }

          int n = 0;
          // WHILE
          while (n < 10000000)
          {
              Console.WriteLine("ML App Embed Python gRPC Server!");
              n++;
          }

          // AFTER
          using (Py.GIL())
          {
              server.wait_for_termination();
          }

          using (Py.GIL())
          {
              server.stop(true);
              Console.WriteLine($"gRPC server ending...");
          }
      }
  ```

  when run into `WHILE`, the client gRPC will suspend. While run into `AFTER`, the client gRPC will get response.

  It is suspected that when running C# code, the python code context will be put aside no matter python start a new process.

  Seeing project at [MLAppModuleServer](MLAppEmbedServer/MLAppModuleServer/Program.cs)

  - .NET starts a process to import gRPC server module and run the server(no)
    It seem not possible to use .NET `Process` to do this operation.

  - .NET starts a process to run server script/module(yes)
    It works. In addition, the process can be kiiled from .NET.

    ```c#
    // start process
    using (Process process = Process.Start(startInfo))
    {
        Console.WriteLine($"process.HasExited: {process.HasExited}");
        //Thread.Sleep(3000000);

        // start dummy main window application
        WindowApplication();
        Console.WriteLine($"process.HasExited: {process.HasExited}");

        // stop process
        process.Kill();
        Console.WriteLine($"process.HasExited: {process.HasExited}");
    }
    ```

    When `start process`, python server will start.
    When `start dummy main window application`, .NET App will exit the `WindowApplication()` until press `Exit`. And if press `Enter`, .NET App will send a prediction request through gRPC.
    When `stop process`, python server will stop. Then .NET App exit.

    Seeing project at [MLAppProcessServer](MLAppEmbedServer/MLAppProcessServer/Program.cs)

    **TODO**

    - Redirect the process output to the .NET App. It could help debug python server, although we could see the log file of python server.

    - Enusre killing process when .NET App crash.
      When .NET crashed, it will encounter the process alive but the .NET App terminated. So the process must be killed manually.

## Relative Additional

[.NET Core Process](https://docs.microsoft.com/en-us/dotnet/api/system.diagnostics.process?view=netcore-3.1)
