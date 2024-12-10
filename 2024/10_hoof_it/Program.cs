
string[] lines = File.ReadAllLines("10_input.txt");
char[,] grid = new char[lines.Length, lines[0].Length];
List<(int Y, int X)> starts = [];

for (int i = 0; i < lines.Length; i++)
{
    for (int j = 0; j < lines[i].Length; j++)
    {
        if (lines[i][j] == '0')
        {
            starts.Add((i, j));
        }

        grid[i, j] = lines[i][j];
    }
}

Console.WriteLine($"part1: {Solve(grid, starts, true)}");
Console.WriteLine($"part2: {Solve(grid, starts, false)}");

static long Solve(char[,] grid, List<(int Y, int X)> starts, bool unique)
{
    int total = 0;
    Queue<(int Y, int X)> queue = new();
    HashSet<(int Y, int X)> visited = new();

    for (int i = 0; i < starts.Count; i++)
    {
        queue.Enqueue(starts[i]);
        visited.Clear();

        while (queue.Count > 0)
        {
            var pos = queue.Dequeue();
            if (unique && !visited.Add(pos))
                continue;

            char curr = GetPosition(grid, pos);
            if (curr == '9')
            {
                total++;
                continue;
            }

            curr++;
            if (GetPosition(grid, (pos.Y - 1, pos.X)) == curr)
                queue.Enqueue((pos.Y - 1, pos.X));

            if (GetPosition(grid, (pos.Y + 1, pos.X)) == curr)
                queue.Enqueue((pos.Y + 1, pos.X));

            if (GetPosition(grid, (pos.Y, pos.X - 1)) == curr)
                queue.Enqueue((pos.Y, pos.X - 1));

            if (GetPosition(grid, (pos.Y, pos.X + 1)) == curr)
                queue.Enqueue((pos.Y, pos.X + 1));
        }
    }

    return total;
}

static char GetPosition(char[,] grid, (int Y, int X) pos)
{
    if (pos.Y < 0 || pos.Y >= grid.GetLength(0) || pos.X < 0 || pos.X >= grid.GetLength(1))
        return '#';

    return grid[pos.Y, pos.X];
}
