using System;
using System.Diagnostics;
using System.ComponentModel;
using System.Threading;

namespace MyProcessSample
{
    class MyProcess
    {
        // Opens the Internet Explorer application.
        void OpenApplication(string myFavoritesPath)
        {
            // Start Internet Explorer. Defaults to the home page.
            //Process.Start("IExplore.exe");
            // open http://google.com/ in mac
            Process.Start("open", myFavoritesPath);

            // Display the contents of the favorites folder in the browser.
            //Process.Start(myFavoritesPath);
        }

        // Opens urls and .html documents using Internet Explorer.
        void OpenWithArguments()
        {
            // url's are not considered documents. They can only be opened
            // by passing them as arguments.
            Process.Start("open", "http://www.northwindtraders.com");

            // Start a Web page using a browser associated with .html and .asp files.
            //Process.Start("open", "C:\\myPath\\myFile.htm");
            //Process.Start("open", "C:\\myPath\\myFile.asp");
        }

        // Uses the ProcessStartInfo class to start new processes,
        // both in a minimized mode.
        void OpenWithStartInfo()
        {
            ProcessStartInfo startInfo = new ProcessStartInfo("open");
            startInfo.WindowStyle = ProcessWindowStyle.Minimized;

            startInfo.Arguments = "http://www.northwindtraders.com";

            Process.Start(startInfo);
        }


        static void Main()
        {
            // Get the path that stores favorite links.
            string myFavoritesPath =
                Environment.GetFolderPath(Environment.SpecialFolder.Favorites);

            MyProcess myProcess = new MyProcess();

            myProcess.OpenApplication(myFavoritesPath);
            myProcess.OpenWithArguments();
            myProcess.OpenWithStartInfo();

            // OpenThenClose
            using (Process process = Process.Start("subl"))
            {
                // Display physical memory usage 5 times at intervals of 2 seconds.
                for (int i = 0; i < 5; i++)
                {
                    Console.WriteLine($"i:{i}");
                    if (!process.HasExited)
                    {
                        // Discard cached information about the process.
                        process.Refresh();
                        // Print working set to console.
                        Console.WriteLine($"Physical Memory Usage: {process.WorkingSet}");
                        // Wait 2 seconds.
                        Thread.Sleep(2000);
                    }
                    else
                    {
                        break;
                    }
                }

                Console.WriteLine($"process.HasExited: {process.HasExited}");
                // Close process by sending a close message to its main window.
                process.CloseMainWindow();
                // Free resources associated with process.
                process.Close();
            }
        }
    }
}