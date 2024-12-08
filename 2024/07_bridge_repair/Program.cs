List<(long, int[])> input = [];
foreach (string line in File.ReadLines("07_input.txt"))
{
    string[] split = line.Split(' ');
    long total = long.Parse(split[0].Trim(':'));
    int[] parts = split[1..].Select(int.Parse).ToArray();
    input.Add((total, parts));
}

Console.WriteLine($"Part 1: {Part1(input):n0}");
Console.WriteLine($"Part 2: {Part2(input):n0}");


static long Part1(List<(long, int[])> input)
{
    long result = 0;

    foreach ((long total, int[] parts) in input)
    {
        result += Part1Recursive(total, parts, parts[0], 1);
    }

    return result;
}

static long Part2(List<(long, int[])> input)
{
    long result = 0;

    foreach ((long total, int[] parts) in input)
    {
        result += Part2Recursive(total, parts, parts[0], 1);
    }

    return result;
}

static long Part1Recursive(long total, int[] parts, long curr, int index)
{
    if (index == parts.Length)
        return total == curr ? total : 0;

    long plus = Part1Recursive(total, parts, curr + parts[index], index + 1);
    if (plus != 0)
        return plus;

    long mult = Part1Recursive(total, parts, curr * parts[index], index + 1);
    if (mult != 0)
        return mult;

    return 0;
}

static long Part2Recursive(long total, int[] parts, long curr, int index)
{
    if (index == parts.Length)
        return total == curr ? total : 0;

    long plus = Part2Recursive(total, parts, curr + parts[index], index + 1);
    if (plus != 0)
        return plus;

    long mult = Part2Recursive(total, parts, curr * parts[index], index + 1);
    if (mult != 0)
        return mult;

    int digitCount = (int)Math.Floor(Math.Log10(Math.Abs(parts[index])) + 1);
    int power10 = (int)Math.Pow(10, digitCount);
    long concatenated = curr * power10 + parts[index];

    long concat = Part2Recursive(total, parts, concatenated, index + 1);
    if (concat != 0)
        return concat;

    return 0;
}
