string[] lines = File.ReadAllLines("02_input.txt");

bool safe = IsSafe([17, 18, 15, 13, 12, 10], 1);

int total = 0;
foreach (string line in lines)
{
    int[] levels = line.Split(' ').Select(int.Parse).ToArray();

    bool isSafe = IsSafe(levels, 1);
    Console.Write(string.Join(" ", levels) + " - ");
    Console.WriteLine(isSafe ? "Safe" : "Unsafe");

    if (isSafe)
        total++;
}

Console.WriteLine("Total safe: " + total);

static bool IsSafe(int[] levels, bool skipAllowed)
{
    int? skipIndex = null;
    bool? negative = null;
    for (int i = 0; i < levels.Length - 1; i++)
    {
        if (!IsSingleSafe(levels[i], levels[i + 1], ref negative))
        {
            if (!skipAllowed)
                return false;
            skipAllowed = false;

            if (i > 0 && i + 2 < levels.Length)
            {
                if (!IsSingleSafe(levels[i], levels[i + 2], ref negative))
                    return false;
            }
        }
    }

    return true;
}

static bool IsSingleSafe(int number1, int number2, ref bool? negative)
{
    int diff = number1 - number2;
    if (diff == 0 || Math.Abs(diff) > 3)
        return false;

    if (diff > 0)
    {
        if (negative == true)
            return false;

        negative = false;
    }
    else if (diff < 0)
    {
        if (negative == false)
            return false;

        negative = true;
    }

    return true;
}
