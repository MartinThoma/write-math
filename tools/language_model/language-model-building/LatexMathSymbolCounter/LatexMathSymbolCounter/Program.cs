using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace LatexMathSymbolCounter
{
    class Program
    {
        static void Main(string[] args)
        {
            handledFiles = new HashSet<string>();
            cachedFiles = new Dictionary<string, List<LatexToken>>();
            removeQueue = new List<string>();
            resultCounters = new Dictionary<string, int>();

            if (args.Length != 1)
            {
                Console.WriteLine("Usage: lmsc.exe [ Filename | Directorypath ]");

            }
            else
            {
                if ((File.GetAttributes(args[0]) & FileAttributes.Directory) == 0)
                {
                    ReadLatexFile(args[0], true, true);
                }
                else
                {
                    ParseDirectory(args[0]);
                }

                if (resultCounters.Any())
                {
                    Console.WriteLine("{");
                    var counters = resultCounters.OrderByDescending(x => x.Value).ToArray();
                    string last = counters.Last().Key;
                    foreach (KeyValuePair<string, int> counter in counters)
                    {
                        Console.Write("   \"" + counter.Key + "\": " + counter.Value);
                        if (counter.Key == last)
                            Console.WriteLine();
                        else
                            Console.WriteLine(",");
                    }
                    Console.WriteLine("}");
                }
                else
                {
                    Console.WriteLine("No results.");
                }
            }

            Console.ReadKey();
        }

        const string LatexFileEnding = ".tex";
        const string PackageFileEnding = ".sty";
        string[] ValidFileEndings = { PackageFileEnding, LatexFileEnding };

        static HashSet<string> handledFiles;
        static Dictionary<string, List<LatexToken>> cachedFiles;
        static List<string> removeQueue;

        static Dictionary<string, int> resultCounters; 

        static void ParseDirectory(string root)
        {
            foreach (string file in Directory.GetFiles(root))
            {
                if (Path.GetExtension(file) == LatexFileEnding)
                {
                    if (!handledFiles.Contains(file.ToLower()) && !cachedFiles.ContainsKey(file.ToLower()))
                    {
                        ReadLatexFile(file, true);
                    }
                }
            }

            foreach (string file in Directory.GetDirectories(root))
            {
                ParseDirectory(file);
            }
        }

        static void ReadLatexFile(string file, bool rootAllowed = true, bool forceProcess = false)
        {
            Console.Error.WriteLine(file);

            string value = File.ReadAllText(file);

            LatexReader reader = new LatexReader(value);

            List<LatexToken> texFile = reader.ReadTokens(new char[0]);
            if (reader.Peek() != -1)
                System.Diagnostics.Debugger.Break();

            if ((IsRoodDocument(texFile) && rootAllowed) || forceProcess)
            {
                ResolveInputs(texFile, Path.GetDirectoryName(file), file);

                FlattenBegin(texFile, "math");
                FlattenBegin(texFile, "equation");
                FlattenBegin(texFile, "align");
                FlattenBegin(texFile, "align*");

                var defines = FindDefines(new Dictionary<string, List<LatexToken>>(), texFile);

                RemoveRecursiveDefines(defines);

                foreach (List<LatexToken> define in defines.Values)
                {
                    ExpandCommands(defines, define);
                }

                ExpandCommands(defines, texFile);

                CountCommands(resultCounters, texFile, true, false);
                
                removeQueue.Add(file.ToLower());

                foreach (string handledFile in removeQueue)
                {
                    handledFiles.Add(file);
                    cachedFiles.Remove(file);
                }
                removeQueue.Clear();

            }
            else
            {
                cachedFiles.Add(file.ToLower(), texFile);
            }
        }

        private static void RemoveRecursiveDefines(Dictionary<string, List<LatexToken>> defines)
        {
            foreach (KeyValuePair<string, List<LatexToken>> define in defines.ToArray())
            {
                if (ContainsCommand(define.Key, define.Value))
                    defines.Remove(define.Key);
            }
        }

        private static bool ContainsCommand(string command, List<LatexToken> input)
        {
            foreach (LatexToken t in input)
            {
                if (t.Value == command && t.Type == LatexTokenType.Command)
                    return true;

                if (ContainsCommand(command, t.Children))
                    return true;
            }

            return false;
        }

        static void FlattenBegin(List<LatexToken> input, string key)
        {
            int beginIndex = -1;
            int endIndex = -1;

            for(int i = 0; i < input.Count; i++)
            {
                LatexToken token = input[i];

                if (token.Children.Count != 0 && token.Children[0].Children.Count != 0)
                {
                    if (token.Type == LatexTokenType.Command && token.Value == "\\begin" &&
                       token.Children[0].Type == LatexTokenType.CurlyBraces && token.Children[0].Children[0].Value == key)
                    {
                        if (beginIndex != -1)
                        {
                            throw new ArgumentException("Found nested math env.");
                        }
                        beginIndex = i;
                    }
                    if (token.Type == LatexTokenType.Command && token.Value == "\\end" &&
                       token.Children[0].Type == LatexTokenType.CurlyBraces && token.Children[0].Children[0].Value == key)
                    {
                        if (beginIndex == -1)
                        {
                            throw new ArgumentException("Found end math at wrong level.");
                        }
                        endIndex = i;
                        List<LatexToken> newChildren = input.Skip(beginIndex + 1).Take(endIndex - beginIndex - 1).ToList();
                        foreach (LatexToken toRemove in newChildren)
                        {
                            input.Remove(toRemove);
                        }
                        input.RemoveAt(beginIndex);
                        input.RemoveAt(beginIndex);
                        input.Insert(beginIndex, new LatexToken() { Type = LatexTokenType.Math, Children = newChildren });

                        i = beginIndex;
                        token = input[i];
                        beginIndex = -1;
                        endIndex = -1;
                    }
                }

                if (token.Children != null)
                {
                    FlattenBegin(token.Children, key);
                }
            }
        }

        static void ExpandCommands(Dictionary<string, List<LatexToken>> defines, List<LatexToken> document)
        {
            bool expanding = true;

            while (expanding)
            {
                expanding = false;

                foreach (LatexToken token in document)
                {
                    if (token.Type == LatexTokenType.Command && defines.ContainsKey(token.Value))
                    {
                        token.Children.AddRange(defines[token.Value]);
                        token.Value = "$expanded[" + token.Value + "]$";
                        token.Type = LatexTokenType.Unknown;
                        expanding = true;
                    }
                }
            }

            foreach (LatexToken token in document)
            {
                ExpandCommands(defines, token.Children);
            }
        }

        static Dictionary<string, List<LatexToken>> FindDefines(Dictionary<string, List<LatexToken>> defines, List<LatexToken> document)
        {
            for(int i = 0; i < document.Count; i++)
            {
                LatexToken token = document[i];
                if (token.Type == LatexTokenType.Command && token.Value == "\\newcommand")
                {
                    try
                    {
                        string command;
                        List<LatexToken> newToken;
                        if (i + 1 >= document.Count || document[i + 1].Value != "*")
                        {
                            if (token.Children.Count > 0)
                            {
                                command = token.Children[0].Children[0].Value;
                                newToken = token.Children[1].Children;
                            }
                            else
                            {
                                command = document[i + 1].Value;
                                newToken = document[i + 1].Children[0].Children;
                            }
                        }
                        else
                        {
                            if (document[i + 2].Type == LatexTokenType.CurlyBraces)
                            {
                                command = document[i + 2].Children[0].Value;
                                newToken = document[i + 3].Children;
                            }
                            else
                            {
                                command = document[i + 2].Value;
                                newToken = document[i + 2].Children[0].Children;
                            }
                        }

                        if (!defines.ContainsKey(command))
                        {
                            defines.Add(command, newToken);
                        }
                    }
                    catch (Exception ex) { }

                    token.Value = "$handlednewcommand$";
                }
                if(token.Type == LatexTokenType.Command && token.Value == "\\def") {
                    try
                    {
                        if (document[i + 1].Type != LatexTokenType.Command)
                            throw new InvalidOperationException("Expected Def declaration");
                        string command = document[i + 1].Value;

                        var braces = document[i + 1].Children.Find(x => x.Type == LatexTokenType.CurlyBraces);

                        if (braces == null)
                            throw new InvalidOperationException("Expected Def declaration");

                        List<LatexToken> newToken = braces.Children;

                        if (!defines.ContainsKey(command))
                        {
                            defines.Add(command, newToken);
                        }
                    }
                    catch (Exception ex) { }

                    token.Value = "$handledef$";
                }
                FindDefines(defines, token.Children);
            }

            return defines;
        }

        static Dictionary<string, int> CountCommands(Dictionary<string, int> commands, List<LatexToken> command, bool mathOnly = false, bool isInMath = false)
        {
            for(int i = 0; i < command.Count; i++)
            {
                LatexToken token = command[i];

                if (token.Type == LatexTokenType.Command && (isInMath || !mathOnly))
                {
                    string cmd = token.Value;
                    if (token.Children.Count > 0 && token.Children[0].Type == LatexTokenType.CurlyBraces && token.Children[0].Children.Count > 0)
                    {
                        cmd += "{" + token.Children[0].Children[0].Value + "}";
                    }

                    if (!commands.ContainsKey(cmd))
                        commands.Add(cmd, 0);

                    commands[cmd]++;
                } 
                
                if (token.Type == LatexTokenType.Math)
                {
                    CountCommands(commands, token.Children, mathOnly, true);
                }
                else
                {
                    CountCommands(commands, token.Children, mathOnly, isInMath);
                }
            }

            return commands;
        }

        static List<LatexToken> GetFileForRootAttach(string file)
        {
            if (!cachedFiles.ContainsKey(file.ToLower()))
            {
                ReadLatexFile(file, false);
            }

            ResolveInputs(cachedFiles[file.ToLower()], Path.GetDirectoryName(file), file);

            removeQueue.Add(file.ToLower());

            return cachedFiles[file.ToLower()];
        }
        static void ResolveInputs(List<LatexToken> doc, string dirPath, string sourcePath)
        {
            var inputs = doc.Where(x => x.Type == LatexTokenType.Command && x.Value == "\\input");

            foreach(LatexToken inputCommand in inputs)
            {
                if (inputCommand.Children.Count == 0)
                    continue;
                var bracket = inputCommand.Children[0];
                if(!bracket.Children.Any())
                    continue;

                string inputPath = bracket.Children[0].Value;
                try
                {
                    inputPath = ResolveTex(inputPath, dirPath);
                    inputCommand.Value = "$$includedinput$$";
                    inputCommand.Type = LatexTokenType.Unknown;
                    if(sourcePath.ToLower() != inputPath.ToLower())
                        inputCommand.Children.AddRange(GetFileForRootAttach(inputPath));
                }
                catch (FileNotFoundException ex)
                {
                    //Console.WriteLine("Error: Included file missing " + inputPath);
                }
            }

            var styles = doc.Where(x => x.Type == LatexTokenType.Command && x.Value == "\\usepackage");

            foreach (LatexToken usepackageCommand in styles)
            {
                var bracket = usepackageCommand.Children.Find(x => x.Type == LatexTokenType.CurlyBraces);

                if (bracket == null || !bracket.Children.Any())
                    continue;

                string fileName = bracket.Children[0].Value;

                try
                {
                    string inputPath = ResolveSty(fileName, dirPath);
                    usepackageCommand.Value = "$$includedusepackage$$";
                    usepackageCommand.Type = LatexTokenType.Unknown;
                    if (sourcePath.ToLower() != inputPath.ToLower())
                        usepackageCommand.Children.AddRange(GetFileForRootAttach(inputPath));
                }
                catch (FileNotFoundException ex)
                {
                    //Console.WriteLine("Skipped include of usepackage " + fileName);
                }
            }

            foreach (LatexToken child in doc)
            {
                ResolveInputs(child.Children, dirPath, sourcePath);
            }
        }

        static bool IsRoodDocument(List<LatexToken> doc)
        {
            return doc.Find(x => x.Type == LatexTokenType.Command && x.Value == "\\documentclass") != null;
        }

        static string ResolveTex(string name, string currentPath)
        {
            return Resolve(name, currentPath, "tex");
        }

        static string ResolveSty(string name, string currentPath)
        {
            return Resolve(name, currentPath, "sty");
        }

        static string Resolve(string name, string currentPath, string ending)
        {
            string path = Path.Combine(currentPath, name);
            if (File.Exists(path))
                return path;

            path = Path.Combine(currentPath, name + "." + ending);
            if (File.Exists(path))
                return path;

            throw new FileNotFoundException("Input file not found.");
        }
    }
}
