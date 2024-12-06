using System.Diagnostics;

string[] lines = File.ReadAllLines("../../../06_input.txt");

(int Y, int X)[] directions = [(-1, 0), (0, 1), (1, 0), (0, -1)];

char[,] grid = new char[lines.Length, lines[0].Length];

int startY = -1, startX = -1;

for (int i = 0; i < lines.Length; i++)
{
    for (int j = 0; j < lines[i].Length; j++)
    {
        if (lines[i][j] == '^')
        {
            startY = i;
            startX = j;
        }

        grid[i, j] = lines[i][j];
    }
}

// Print grid
Console.WriteLine($"part1: {Part1(grid, startY, startX)}");
Stopwatch sw = Stopwatch.StartNew();
int part2 = Part2(grid, startY, startX);
sw.Stop();

Console.WriteLine($"part2: {part2}, elapsed: {sw.Elapsed}");

int Part1(char[,] grid, int startY, int startX)
{
    HashSet<(int, int)> visited = [];

    (int Y, int X) curr = (startY, startX);
    int direction = 0;

    while (true)
    {
        visited.Add(curr);
        (int Y, int X) next = (curr.Y + directions[direction].Y, curr.X + directions[direction].X);
        if (next.Y < 0 || next.Y >= grid.GetLength(0) || next.X < 0 || next.X >= grid.GetLength(1))
            break;

        if (grid[next.Y, next.X] == '#')
        {
            direction = (direction + 1) % 4;
            continue;
        }

        curr = next;
    }

    return visited.Count;
}

int Part2(char[,] grid, int startY, int startX)
{
    int total = 0;

    Parallel.For(0, grid.GetLength(0), i =>
    {
        for (int j = 0; j < grid.GetLength(1); j++)
        {
            HashSet<(int, int, int)> visited = [];
            (int Y, int X) curr = (startY, startX);
            int direction = 0;

            while (true)
            {
                if (!visited.Add((curr.Y, curr.X, direction)))
                {
                    Interlocked.Increment(ref total);
                    break;
                }

                (int Y, int X) next = (curr.Y + directions[direction].Y, curr.X + directions[direction].X);
                if (next.Y < 0 || next.Y >= grid.GetLength(0) || next.X < 0 || next.X >= grid.GetLength(1))
                    break;

                if (grid[next.Y, next.X] == '#' || (next.Y == i && next.X == j))
                {
                    direction = (direction + 1) % 4;
                    continue;
                }

                curr = next;
            }
        }
    });

    return total;
}
