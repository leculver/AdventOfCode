string[] input = File.ReadAllLines("input.txt");

int total = 0;

foreach (string line in input)
{
    int first = int.MinValue;
    int last = 0;
    for (int i = 0; i < line.Length; i++)
    {
        if ('0' <= line[i] && line[i] <= '9')
        {
            last = line[i] - '0';
            if (first == int.MinValue)
                first = last;
        }
    }

    total += first * 10 + last;
}

Console.WriteLine(total);

Dictionary<string, int> numbers = new()
{
    {"zero", 0 },
    {"one", 1 },
    {"two", 2 },
    {"three", 3 },
    {"four", 4 },
    {"five", 5 },
    {"six", 6 },
    {"seven", 7 },
    {"eight", 8 },
    {"nine", 9 },
};

total = 0;
foreach (string line in input)
{
    int first = int.MinValue;
    int last = 0;
    for (int i = 0; i < line.Length; i++)
    {
        if ('0' <= line[i] && line[i] <= '9')
        {
            last = line[i] - '0';
            if (first == int.MinValue)
                first = last;
        }
        else
        {
            ReadOnlySpan<char> span = line.AsSpan(i);
            foreach (string key in numbers.Keys)
            {
                if (span.StartsWith(key))
                {
                    last = numbers[key];
                    if (first == int.MinValue)
                        first = last;
                    break;
                }
            }
        }
    }

    total += first * 10 + last;
}

Console.WriteLine(total);
