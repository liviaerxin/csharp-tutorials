using System;
using System.Collections.Generic;
using Python.Runtime;
using System.Threading;


namespace MLAppModuleServer
{
    class Program
    {

        static void Main(string[] args)
        {
            RunGRPC();
        }


        public static void RunFlask()
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
                dynamic flask_server = Py.Import("sentiment_analysis.flask_server");

                server = flask_server.WrapperServer();

                server.start();
                Console.WriteLine($"Flask server starting...");

                //server.stop(true);
            }

            while (true)
            {
                Console.WriteLine("ML App Embed Python gRPC Server!");
            }
        }


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

                server.start();
                Console.WriteLine($"gRPC server starting...");

            }

            int n = 0;
            while (n < 1000000)
            {
                Console.WriteLine("ML App Embed Python gRPC Server!");
                n++;
            }

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
    }
}
