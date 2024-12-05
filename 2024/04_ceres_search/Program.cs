using System.Diagnostics;
using TorchSharp;
using static TorchSharp.torch;

InitializeDeviceType(DeviceType.CUDA);

string[] lines = File.ReadAllLines("04_input.txt");

// Increase the input lines by a factor.
const int mult = 25;
string[] newLines = new string[lines.Length * mult];
for (int i = 0; i < lines.Length; i++)
    for (int j = 0; j < mult; j++)
        newLines[i * mult + j] = lines[i];

lines = newLines;

char[,] multidim = new char[lines.Length, lines[0].Length];
sbyte[] flat = new sbyte[lines.Length * lines[0].Length];
for (int i = 0; i < lines.Length; i++)
{
    for (int j = 0; j < lines[i].Length; j++)
    {
        multidim[i, j] = lines[i][j];
        flat[i * lines[i].Length + j] = (sbyte)lines[i][j];
    }
}

Console.WriteLine($"Part1: {WordSearch(multidim, "XMAS")}");

Stopwatch sw = Stopwatch.StartNew();
var result = MASSearch(multidim);
sw.Stop();

Console.WriteLine($"Part2: {result} time={sw.Elapsed}");

sw.Restart();
var tensor = CreateMASTensor(flat, multidim.GetLength(0), multidim.GetLength(1));
sw.Stop();

Console.WriteLine($"Create tensor time={sw.Elapsed}");

sw.Restart();
long resultTorch = TorchMASSearch(tensor);
sw.Stop();

var device = torch.cuda.is_available() ? torch.CUDA : torch.CPU;
Console.WriteLine($"Torch:  {resultTorch} time={sw.Elapsed} device={device}");

Console.WriteLine($"Total lines processed = {lines.Length:n0}");

// Part 1
static int WordSearch(char[,] grid, string search)
{
    int count = 0;
    for (int x = 0; x < grid.GetLength(0); x++)
    {
        for (int y = 0; y >= 0 && y < grid.GetLength(1); y++)
        {
            // Search forwards
            if (WordSearchSequenceEqual(grid, search, x, y, 1, 0))
                count++;

            // Search backwards
            if (WordSearchSequenceEqual(grid, search, x, y, -1, 0))
                count++;

            // Search down
            if (WordSearchSequenceEqual(grid, search, x, y, 0, 1))
                count++;

            // Search up
            if (WordSearchSequenceEqual(grid, search, x, y, 0, -1))
                count++;

            // Search down-right
            if (WordSearchSequenceEqual(grid, search, x, y, 1, 1))
                count++;

            // Search down-left
            if (WordSearchSequenceEqual(grid, search, x, y, -1, 1))
                count++;

            // Search up-right
            if (WordSearchSequenceEqual(grid, search, x, y, 1, -1))
                count++;

            // Search up-left
            if (WordSearchSequenceEqual(grid, search, x, y, -1, -1))
                count++;
        }
    }

    return count;
}

static bool WordSearchSequenceEqual(char[,] grid, string search, int x, int y, int dirX, int dirY)
{
    int pos = 0;
    while (pos < search.Length)
    {
        if (x < 0 || x >= grid.GetLength(0) || y < 0 || y >= grid.GetLength(1))
            return false;

        if (grid[x, y] != search[pos])
            return false;

        x += dirX;
        y += dirY;
        pos++;
    }

    return true;
}

// Part 2
static int MASSearch(char[,] grid)
{
    int count = 0;
    for (int x = 1; x < grid.GetLength(0) - 1; x++)
    {
        for (int y = 1; y < grid.GetLength(1) - 1; y++)
        {
            if (grid[x, y] == 'A')
            {
                if (MASEqual(grid, grid[x-1, y-1], grid[x+1, y+1]) &&
                    MASEqual(grid, grid[x-1, y+1], grid[x+1, y-1]))
                    {
                        count++;
                    }
            }
        }
    }

    return count;
}

static Tensor CreateMASTensor(sbyte[] flat, int H, int W)
{
    var tensor = from_array(flat, torch.int8);
    tensor = tensor.view(H, W);

    var device = cuda.is_available() ? torch.CUDA : torch.CPU;
    tensor = tensor.to(device);

    return tensor;
}

static long TorchMASSearch(Tensor wordsearch)
{
    var windows = wordsearch.unfold(0, 3, 1).unfold(1, 3, 1);

    // Middle
    var posA = windows[TensorIndex.Ellipsis, 1, 1] == (sbyte)'A';

    // Top-left to bottom-right diagonal
    var posDiag = (
        windows[TensorIndex.Ellipsis, 0, 0] == (sbyte)'M' &
        windows[TensorIndex.Ellipsis, 2, 2] == (sbyte)'S'
    ) | (
        windows[TensorIndex.Ellipsis, 0, 0] == (sbyte)'S' &
        windows[TensorIndex.Ellipsis, 2, 2] == (sbyte)'M'
    );

    // Top-right to bottom-left diagonal
    var posAnti = (
        windows[TensorIndex.Ellipsis, 2, 0] ==  (sbyte)'M' &
        windows[TensorIndex.Ellipsis, 0, 2] ==  (sbyte)'S'
    ) | (
        windows[TensorIndex.Ellipsis, 2, 0] == (sbyte)'S' &
        windows[TensorIndex.Ellipsis, 0, 2] == (sbyte)'M'
    );

    // Combine conditions
    var result = posA & posDiag & posAnti;

    // Count total matches
    return result.sum().item<long>();
}

static bool MASEqual(char[,] grid, char v1, char v2)
{
    if (v1 > v2)
        (v2, v1) = (v1, v2);

    return v1 == 'M' && v2 == 'S';
}