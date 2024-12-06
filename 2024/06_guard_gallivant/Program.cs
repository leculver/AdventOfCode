using System.Numerics.Tensors;

string[] lines = File.ReadAllLines("../../../06_input.txt");

Tensor<byte> grid = new Tensor<byte>(lines.Length, lines[0].Length);



char end = lines[0].Last();
char[,] grid = new char[lines.Length, lines[0].Length];

int posY = -1, posX = -1;

for (int i = 0; i < lines.Length; i++)
    for (int j = 0; j < lines[i].Length; j++)
    {
        if (lines[i][j] == '^')
        {
            posY = i;
            posX = j;
        }
        else
        {
            grid[i, j] = lines[i][j];
        }
    }

// Print grid
Console.WriteLine($"part1: {PerformWalk(grid, posY, posX)}");

static int PerformWalk(char[,] grid, int posY, int posX)
{
    int dirY = -1, dirX = 0;
    int visited = 0;
    while (true)
    {
        char curr = GetPosition(grid, posY, posX);
        if (curr == 'E')
            break;

        if (curr == '#')
            throw new InvalidOperationException("Should not have reached here.");

        if (curr != 'X')
        {
            visited++;
            grid[posY, posX] = 'X';
        }

        char next = GetPosition(grid, posY + dirY, posX + dirX);
        while (next == '#')
        {
            // make right hand turns
            if (dirY == -1)
            {
                dirX = 1;
                dirY = 0;
            }
            else if (dirX == 1)
            {
                dirX = 0;
                dirY = 1;
            }
            else if (dirY == 1)
            {
                dirX = -1;
                dirY = 0;
            }
            else if (dirX == -1)
            {
                dirX = 0;
                dirY = -1;
            }

            next = GetPosition(grid, posY + dirY, posX + dirY);
        }

        posY += dirY;
        posX += dirX;
    }

    return visited;
}

static char GetPosition(char[,] grid, int posY, int posX)
{
    if (0 <= posX && posX < grid.GetLength(1) && 0 <= posY && posY < grid.GetLength(0))
        return grid[posY, posX];
    return 'E';
}

