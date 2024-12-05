use std::fs;
use std::io;
use std::collections::HashMap;

fn read_two_columns(file_path: &str) -> io::Result<(Vec<i32>, Vec<i32>)>
{
    let contents = fs::read_to_string(file_path)?;
    let mut list_1 = Vec::new();
    let mut list_2 = Vec::new();

    for line in contents.lines()
    {
        let parts : Vec<&str> = line.split_whitespace().collect();
        if parts.len() == 2
        {
            list_1.push(parts[0].parse::<i32>().unwrap());
            list_2.push(parts[1].parse::<i32>().unwrap());
        }
        else
        {
            return Err(io::Error::new(io::ErrorKind::InvalidData, "Invalid data"));
        }
    }

    Ok((list_1, list_2))
}

fn part1(list_1: &Vec<i32>, list_2: &Vec<i32>) -> i32
{
    let mut sorted_1 = list_1.clone();
    let mut sorted_2 = list_2.clone();

    sorted_1.sort();
    sorted_2.sort();

    let mut total = 0;

    for i in 0..sorted_1.len()
    {
        total += (sorted_1[i] - sorted_2[i]).abs();
    }

    total
}

fn part2(list_1: &Vec<i32>, list_2: &Vec<i32>) -> i32
{
    let mut counts = HashMap::new();

    for i in 0..list_2.len()
    {
        *counts.entry(list_2[i]).or_insert(0) += 1;
    }

    let mut total = 0;
    for i in 0..list_1.len()
    {
        total += list_1[i] * counts.get(&list_1[i]).unwrap_or(&0);
    }

    total
}

fn main()
{
    match read_two_columns("01_input.txt")
    {

        Ok((list_1, list_2)) => {
            let part1_result = part1(&list_1, &list_2);
            let part2_result = part2(&list_1, &list_2);
            println!("Part 1: {}", part1_result);
            println!("Part 2: {}", part2_result);
        }
        Err(e) => {
            eprintln!("Error reading file: {}", e);
        }
    }
}
