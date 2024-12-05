use std::fs;
use std::io;

fn read_data(file_path: &str) -> io::Result<Vec<Vec<i32>>>
{
    let contents = fs::read_to_string(file_path)?;
    let mut result = Vec::new();

    for line in contents.lines()
    {
        let mut list = Vec::new();
        let parts : Vec<&str> = line.split_whitespace().collect();
        for part in parts
        {
            list.push(part.parse::<i32>().unwrap());
        }

        result.push(list);
    }

    Ok(result)
}

fn is_valid(list: &Vec<i32>) -> bool
{
    let mut correct = true;
    let decreasing = list[0] > list[1];

    for window in list.windows(2)
    {
        let curr_decrease = window[0] > window[1];
        if curr_decrease != decreasing
        {
            correct = false;
            break;
        }

        let diff = (window[0] - window[1]).abs();
        if diff == 0 || diff > 3
        {
            correct = false;
            break;
        }
    }

    correct
}

fn part1(data: &Vec<Vec<i32>>) -> i32
{
    let mut total = 0;

    for list in data
    {
        if is_valid(list)
        {
            total += 1;
        }
    }

    total
}

fn part2(data: &Vec<Vec<i32>>) -> i32
{
    let mut total = 0;

    for list in data
    {
        if is_valid(list)
        {
            total += 1;
        }
        else
        {
            for i in 0..list.len()
            {
                let mut new_list = list.clone();
                new_list.remove(i);
                if is_valid(&new_list)
                {
                    total += 1;
                    break;
                }
            }
        }
    }

    total
}

fn main()
{
    let file_path = "02_input.txt";
    match read_data(file_path)
    {
        Ok(result) =>
        {
            println!("{}", part1(&result));
            println!("{}", part2(&result));
        },
        Err(e) =>
        {
            eprintln!("Error: {}", e);
        }
    }
}