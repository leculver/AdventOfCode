const string InputFile = "09_input.txt";


Console.WriteLine($"Part 1: {Part1():n0}");
Console.WriteLine($"Part 2: {Part2():n0}");


static long Part1()
{
    (List<int?> filesystem, _) = GetInput();
    int lpos = 0;
    int rpos = filesystem.Count - 1;

    while (lpos < rpos)
    {
        while (filesystem[lpos] != null && lpos < rpos)
            lpos++;

        while (filesystem[rpos] == null && lpos < rpos)
            rpos--;

        while (filesystem[lpos] == null && filesystem[rpos] != null && lpos < rpos)
        {
            (filesystem[lpos], filesystem[rpos]) = (filesystem[rpos], filesystem[lpos]);
            lpos++;
            rpos--;
        }
    }

    return GetChecksum(filesystem);
}

static long Part2()
{
    (List<int?> filesystem, Dictionary<int, (int Pos, int Count)> ranges) = GetInput();

    for (int currId = ranges.Keys.Max(); currId >= 0; currId--)
    {
        (int filePosition, int fileLength) = ranges[currId];
        int slot = FindFittingSlot(filesystem, fileLength);
        if (slot <= filePosition)
        {
            for (int i = 0; i < fileLength; i++)
            {
                filesystem[slot + i] = currId;
                filesystem[filePosition + i] = null;
            }
        }
    }

    return GetChecksum(filesystem);
}

static int FindFittingSlot(List<int?> filesystem, int length)
{
    int lpos = 0;
    while (lpos < filesystem.Count)
    {
        if (filesystem[lpos] == null)
        {
            int rpos = lpos + 1;
            while (rpos < filesystem.Count && filesystem[rpos] == null)
                rpos++;

            if (rpos - lpos >= length)
                return lpos;
            lpos = rpos;
        }
        else
        {
            lpos++;
        }
    }

    return int.MaxValue;
}

static long GetChecksum(List<int?> filesystem)
{
    long checksum = 0;
    for (int i = 0; i < filesystem.Count; i++)
    {
        if (filesystem[i] is int curr)
            checksum += curr * i;
    }

    return checksum;
}

static (List<int?>, Dictionary<int, (int Pos, int Count)>) GetInput()
{
    string input = File.ReadAllText(InputFile);
    List<int?> filesystem = [];
    Dictionary<int, (int Pos, int Count)> ranges = [];

    bool free = false;
    int id = 0;
    foreach (char c in input)
    {
        int num = c - '0';

        if (!free)
            ranges[id] = (filesystem.Count, num);

        for (int i = 0; i < num; i++)
        {
            filesystem.Add(free ? null : id);
        }

        if (!free)
            id++;
        free = !free;
    }

    Console.WriteLine($"Filesystem: {filesystem.Count}");
    return (filesystem, ranges);
}
