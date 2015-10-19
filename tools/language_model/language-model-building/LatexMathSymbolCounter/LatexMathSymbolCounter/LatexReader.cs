using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;

namespace LatexMathSymbolCounter
{
    class LatexReader : StringReader
    {
        public LatexReader(string input)
            : base(input)
        {

        }

        char[] escapeChars = { '\\', '$', '_', '#', '{', '}'};
        char[] whitespace = { '\t', ' ', '\r', '\n' };

        public List<LatexToken> ReadTokens(char[] terminationChars) {

            List<LatexToken> results = new List<LatexToken>();

            while (true)
            {
                int current = this.Read();

                if (current == -1)
                {
                    return results;
                }
                if (terminationChars.Contains((char)current))
                {
                    return results;
                }
                else if (current == '\\')
                {
                    if (escapeChars.Contains((char)this.Peek()))
                    {
                        string value = ReadPlaintext((char)current, false, true);
                        if (results.Any() && results.Last().Type == LatexTokenType.Plaintext)
                        {
                            results.Last().Value += value;
                        }
                        else if (value != "")
                        {
                            results.Add(new LatexToken() { Type = LatexTokenType.Plaintext, Value = value });
                        }
                        
                    }
                    else if (((char)this.Peek()) == '[')
                    {
                        results.Add(new LatexToken() { Type = LatexTokenType.SquareMathBegin });
                        this.Read();
                    }
                    else if (((char)this.Peek()) == ']')
                    {
                        List<LatexToken> mathChildren;

                        int index = results.FindIndex(x => x.Type == LatexTokenType.SquareMathBegin);

                        if (index == -1)
                        {
                            throw new FormatException("Could not find square math begin at same layer.");
                        }

                        mathChildren = results.Skip(index + 1).ToList();
                        results = results.Take(index).ToList();

                        results.Add(new LatexToken() { Type = LatexTokenType.Math, Children = mathChildren });
                        this.Read();
                    }
                    else
                    {
                        string value = ReadPlaintext((char)current, true);
                        if (value != "")
                        {
                            results.Add(new LatexToken() { Type = LatexTokenType.Command, Value = value });
                        }
                    }
                }
                else if (current == '$')
                {
                    bool dd = false;
                    if (((char)this.Peek()) == '$')
                    {
                        dd = true;
                        this.Read();
                    }
                    results.Add(new LatexToken() { Children = ReadTokens(new char[] { '$' }), Type = LatexTokenType.Math });

                    if(dd)
                    {
                        this.Read();
                    }
                }
                else if (current == '[' && results.Any() && results.Last().Type == LatexTokenType.Command && results.Last().Value != "\\in" && results.Last().Value != "\\to")
                {
                    LatexToken newCommand = new LatexToken() { Children = ReadTokens(new char[] { ']' }), Type = LatexTokenType.SquareBraces };
                    results.Last().Children.Add(newCommand);
                }
                else if (current == '{')
                {
                    LatexToken newCommand = new LatexToken() { Children = ReadTokens(new char[] { '}' }), Type = LatexTokenType.CurlyBraces };
                    if (results.Any() && results.Last().Type == LatexTokenType.Command)
                    {
                        results.Last().Children.Add(newCommand);
                    }
                    else
                    {
                        results.Add(newCommand);
                    }
                }
                else if (current == '%')
                {
                    ReadLine();
                    //results.Add(new LatexToken() { Value = ReadLine(), Type = LatexTokenType.Comment });
                }
                else
                {
                    string value = ReadPlaintext((char)current, false);
                    if (results.Any() && results.Last().Type == LatexTokenType.Plaintext)
                    {
                        results.Last().Value += value;
                    }
                    else if (value != "")
                    {
                        results.Add(new LatexToken() { Type = LatexTokenType.Plaintext, Value = value });
                    }
                }
            }
        }

        private string ReadPlaintext(char start, bool terminateOnWhitespace, bool isEscaped = false)
        {
            StringBuilder value = new StringBuilder();
            value.Append(start);

            int peek = this.Peek();
            while (peek != -1 && (IsPlain((char)peek) || isEscaped))
            {
                if (!IsPlain((char)peek))
                    isEscaped = false;

                if (terminateOnWhitespace)
                {
                    if(whitespace.Contains((char)peek)) {
                        break;
                    }
                }
                value.Append((char)this.Read());
                peek = this.Peek();
            }

            return value.ToString().Trim();
        }

        private bool IsPlain(char a)
        {
            return (a >= 'a' && a <= 'z') ||
                   (a >= 'A' && a <= 'Z') ||
                   (a >= '0' && a <= '9') ||
                   a == '@' || a == '#';
        }
    }

    [System.Diagnostics.DebuggerDisplay("{Type} ({Value})")]
    class LatexToken
    {
        public LatexTokenType Type { get; set; }
        public List<LatexToken> Children { get; set; }
        public string Value { get; set; }
        public LatexToken()
        {
            Children = new List<LatexToken>();
        }
    }

    enum LatexTokenType
    {
        CurlyBraces,
        SquareBraces,
        Plaintext,
        Command,
        SquareMathBegin,
        Comment,
        Math,
        Unknown
    }
}
