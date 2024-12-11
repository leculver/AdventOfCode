using System.Diagnostics;
using System.Numerics;

const int MAX_LENGTH = 1_000_000;

string line = File.ReadAllText("../../../11_input.txt").Trim();
List<int> start_stones = line.Split(' ').Select(int.Parse).ToList();

Console.WriteLine(string.Join(", ", start_stones));
Console.WriteLine($"part1: {Part1(start_stones, 25):n0}");
Console.WriteLine($"part2: {Part1(start_stones, 75)}");


static int CountDigits(int number)
{
    return (int)Math.Floor(Math.Log10(number)) + 1;
}

static List<int> ApplyRules(List<int> stones)
{
    List<int> result = [];

    foreach (int stone in stones)
    {
        if (stone == 0)
        {
            result.Add(1);
        }
        else
        {
            int digits = CountDigits(stone);
            if (digits % 2 == 0)
            {
                int half = digits / 2;
                string stoneStr = stone.ToString();
                result.Add(int.Parse(stoneStr.Substring(0, half)));
                result.Add(int.Parse(stoneStr.Substring(half)));
            }
            else
            {
                result.Add(stone * 2024);
            }
        }
    }

    return result;
}

static (List<int> first, List<int> second) SplitList(List<int> list)
{
    int half = list.Count / 2;
    return (list.GetRange(0, half), list.GetRange(half, half));
}

static BigInteger Part1(List<int> stones, int steps)
{
    Stopwatch stopwatch = new Stopwatch();
    stopwatch.Start();

    List<List<int>> curr_stones = [stones];

    for (int i = 0; i < steps; i++)
    {
        Stopwatch iteration_sw = Stopwatch.StartNew();
        List<List<int>> next_stones = [];

        if (curr_stones.Count == 1)
        {
            List<int> result = ApplyRules(curr_stones[0]);
            if (result.Count > MAX_LENGTH)
            {
                (List<int> first, List<int> second) = SplitList(result);
                next_stones.Add(first);
                next_stones.Add(second);
            }
            else
            {
                next_stones.Add(result);
            }
        }
        else
        {
            Parallel.ForEach(curr_stones, stones =>
            {
                List<int> result = ApplyRules(stones);
                if (result.Count > MAX_LENGTH)
                {
                    (List<int> first, List<int> second) = SplitList(result);
                    lock (next_stones)
                    {
                        next_stones.Add(first);
                        next_stones.Add(second);
                    }
                }
                else
                {
                    lock (next_stones)
                        next_stones.Add(result);
                }
            });
        }

        iteration_sw.Stop();
        curr_stones = next_stones;
        BigInteger curr_total = Count(curr_stones);
        Console.WriteLine($"Iteration {i} took {iteration_sw.Elapsed.TotalSeconds} seconds, with {curr_total:n0} stones");
    }

    stopwatch.Stop();
    BigInteger total = Count(curr_stones);
    Console.WriteLine($"Total time: {stopwatch.Elapsed.TotalSeconds} seconds, with {total:n0} stones");

    return total;
}

static BigInteger Count(List<List<int>> curr_stones)
{
    BigInteger total = 0;
    foreach (List<int> stones in curr_stones)
    {
        total += stones.Count;
    }

    return total;
}
