﻿using System;
using System.Diagnostics;
using System.ComponentModel;
using System.Threading;
using System.IO;
using GrpcSentimentAnalysis;
using Grpc.Net.Client;
using Grpc.Core;

namespace MLAppProcessServer
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Use process to run a python server script/module");
            ProcessStartInfo startInfo = new ProcessStartInfo();
            //python interprater location
            startInfo.FileName = "python3";
            //argument with file name and input parameters
            // Directory.GetCurrentDirectory() will cause different behaviour in dotnet and visual studio
            //startInfo.Arguments = string.Format("{0} {1} {2}", Path.Combine(Directory.GetCurrentDirectory(), "calculator.py"), 5, 10);

            // script
            string filepath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "../../../../../tf/app.py");
            Console.WriteLine($"script filepath: {filepath}");
            startInfo.Arguments = string.Format("{0}", filepath);
            // module
            //startInfo.Arguments = string.Format("{0} {1}", "-m", "sentiment_analysis.grpc_server");

            startInfo.UseShellExecute = false;// Do not use OS shell
            startInfo.CreateNoWindow = true; // We don't need new window
            startInfo.RedirectStandardOutput = true;// Any output, generated by application will be redirected back
            startInfo.RedirectStandardError = true; // Any error in standard output will be redirected back (for example exceptions)
            //start.LoadUserProfile = true;

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
        }

        // mock a window application. Normally a window app will block the main thread util exit, here
        public static void WindowApplication()
        {
            Console.WriteLine("Start a window application");
            Console.WriteLine("Press 'Enter' key to send prediction request via gRPC");
            Console.WriteLine("Press 'Exit' key to exist");

            bool isExit = false;

            while (!isExit)
            {
                while (Console.KeyAvailable == false)
                    Thread.Sleep(250); // Loop until input is entered.

                ConsoleKey input = Console.ReadKey(true).Key;

                Console.WriteLine($"You pressed the {input} key");

                if (input == ConsoleKey.Escape)
                {
                    isExit = true;
                }
                else if (input == ConsoleKey.Enter)
                {
                    Console.WriteLine($"Sending prediction request via gRPC...");
                    Predict();
                }
                else
                {
                    Console.WriteLine($"Please press 'Exit' or others.");
                }
            }

            Console.WriteLine("Exit the window application.");

        }

        public static void Predict()
        {
            Console.WriteLine("Start gRPC client...");

            // Call insecure gRPC services with .NET Core client, visit https://docs.microsoft.com/en-us/aspnet/core/grpc/troubleshoot?view=aspnetcore-3.1#call-insecure-grpc-services-with-net-core-client
            // This switch must be set before creating the GrpcChannel/HttpClient.
            AppContext.SetSwitch(
                "System.Net.Http.SocketsHttpHandler.Http2UnencryptedSupport", true);

            // The port number(5001) must match the port of the gRPC server.
            using var channel = GrpcChannel.ForAddress("http://localhost:50051");
            try
            {
                var client = new SentimentAnalysis.SentimentAnalysisClient(channel);
                var reply = client.Predict(
                                  new PredictRequest { Text = "the film is really good" });
                Console.WriteLine($"PredictResponse: positive: {reply.Positive}, confidence: {reply.Confidence}, elapsed_time:{reply.ElapsedTime}");
            }
            catch (RpcException ex) when (ex.StatusCode == StatusCode.PermissionDenied)
            {
                Console.WriteLine($"User does not have permission to view this portfolio.");
            }
            catch (RpcException)
            {
                // Handle any other error type ...
                Console.WriteLine($"the gPRC server maybe not startup, please wait few seconds to try again.");
            }
        }
    }
}