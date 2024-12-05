ReadOnlySpan<char> data = File.ReadAllText("03_input.txt").AsSpan();
ReadOnlySpan<char> do_instruction = "do()".AsSpan();
ReadOnlySpan<char> dont_instruction = "don't()".AsSpan();

const bool process_do = true;

int total = 0;

int min_len = "mul(1,1)".Length;
int i = 0;
bool enabled = true;
while (i < data.Length - min_len + 1)
{
    int start = i;

    if (!enabled)
    {
        if (data[i] == 'd' && data.Slice(i, do_instruction.Length).SequenceEqual(do_instruction))
        {
            i += do_instruction.Length;
            enabled = true;
        }
        else
        {
            i++;
            continue;
        }
    }

    if (process_do && data[i] == 'd' && data.Slice(i, dont_instruction.Length).SequenceEqual(dont_instruction))
    {
        i += dont_instruction.Length;
        enabled = false;
        continue;
    }

    if (data[i++] != 'm')
            continue;

    if (data[i] != 'u' && data[i + 1] != 'l' && data[i + 2] != '(')
        continue;

    i += 3;
    bool success = GetNumber(data[i..], out int first, out int offset);
    i += offset;
    if (!success)
        continue;

    if (data[i] != ',')
        continue;

    i++;

    success = GetNumber(data[i..], out int second, out offset);
    i += offset;
    if (!success)
        continue;

    if (data[i] != ')')
        continue;

    i++;

    total += first * second;
    Console.WriteLine($"{data[start..i]} = {first} * {second} = {first * second}, total = {total:n0}");
}

Console.WriteLine($"Total: {total:n0}");

static bool GetNumber(ReadOnlySpan<char> pos, out int number, out int i)
{
    number = 0;
    i = 0;
    bool result = false;
    bool negative = false;

    if (pos[i] == '-')
    {
        i++;
        negative = true;
    }

    while ('0' <= pos[i] && pos[i] <= '9')
    {
        result = true;
        number = number * 10 + (pos[i] - '0');
        i++;
    }

    if (negative)
        number = -number;

    return result;
}
