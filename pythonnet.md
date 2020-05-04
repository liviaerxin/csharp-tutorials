# Pythonnet

## Preparation

Download `https://github.com/pythonnet/pythonnet`

Use `pythonnet` to generate two DLLs:

- `clr.pyd` (clr.so or clr.dylib on Linux and OSX): embed .NET in CPython.
- `Python.Runtime.dll`: embed CPython in .NET.

! when using `pip install pythonnet`, the `clr.pyd` is viable, but `Python.Runtime.dll` does not work.

## Call .NET from Python

## Call Python from .NET

Windows:

Mac OSX:

1. Clone the pythonnet repo (https://github.com/pythonnet/pythonnet)
2. In the pythonnet folder, `cd src\runtime`
3. Run `dotnet build -c ReleaseMonoPY3 -f netstandard2.0 Python.Runtime.15.csproj`
4. Use the built DLL `bin\netstandard2.0\Python.Runtime.dll` as DLL reference, add the belowing into `*.csproj` file,

   ```csproj
   <ItemGroup>
       <Reference Include="Python.Runtime">
           <HintPath>*/bin/netstandard2.0/Python.Runtime.dll</HintPath>
       </Reference>
   </ItemGroup>
   ```

5. Set `DYLD_LIBRARY_PATH` as follows(`LD_LIBRARY_PATH` in linux):

   ```sh
   export DYLD_LIBRARY_PATH=/Library/Frameworks/Python.framework/Versions/3.7/lib
   ```

6. Run the test code

   ```c#
    using System;
    using Python.Runtime;

    namespace Python_CSharp
    {
        class Program
        {
            static void Main(string[] args)
            {
                using (Py.GIL())
                {
                    dynamic os = Py.Import("os");
                    dynamic dir = os.listdir();
                    Console.WriteLine(dir);

                    foreach (var d in dir)
                    {
                        Console.WriteLine(d);
                    }
                }
            }
        }
    }
   ```

**Note:**
Setting `DYLD_LIBRARY_PATH` or `LD_LIBRARY_PATH` maybe be considered harmful, so a better solution for step 5 aimed to add shared libraries can be running `ldconfig` method in Linux and linking to `/usr/local/lib` in Mac. For looking into the depth, there are following useful resources.

Linux:
[Set LD_LIBRARY_PATH correctly](https://unix.stackexchange.com/questions/462755/set-ld-library-path-correctly)

[How to add shared libraries to Linux](https://blog.andrewbeacock.com/2007/10/how-to-add-shared-libraries-to-linuxs.html)

[When should I set LD_LIBRARY_PATH?](http://linuxmafia.com/faq/Admin/ld-lib-path.html)

Mac:
create a symbol link `libpython3.7m.dylib` in `/usr/local/lib`:

1. cd `/usr/local/lib` directory.
2. create a the link `libpython3.7m.dylib` by `ln -s ../../../Library/Frameworks/Python.framework/Versions/3.7/Python libpython3.7m.dylib`

[Using Dynamic Libraries](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/DynamicLibraries/100-Articles/UsingDynamicLibraries.html) !The standard locations for dynamic libraries are `~/lib`, `/usr/local/lib`, and `/usr/lib`.

## References

[pythonnet - Python for .NET](https://github.com/pythonnet/pythonnet)

[Compile Python.Runtime.dll](https://stackoverflow.com/questions/53628176/call-python-script-from-net-core-using-pythonnet/56085756#56085756) !work on windows
