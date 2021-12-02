use std::fs;
use std::collections::VecDeque;

fn part_a(content: &String) -> i32 {
    let mut total = 0i32;
    let mut prev = i32::MAX;

    for line in content.lines() {
        let number: i32 = line.parse().unwrap();
        if number > prev {
            total += 1;
        }
        prev = number;
    }
    return total;
}

fn part_b(content: &String) -> i32 {
    let mut window: VecDeque<i32> = VecDeque::new();
    let mut numbers: Vec<i32> = Vec::new();
    let window_size = 3;

    // Read the lines as numbers
    // Can this be done more idiomatic in rust?
    for line in content.lines() {
        numbers.push(line.parse().unwrap());
    }
    numbers.reverse();

    // Fill the window initially
    for _ in 0..window_size {
        window.push_back(numbers.pop().expect("Not enough numbers to fill initial window"));
    }

    // Actually check
    let mut total = 0;
    let mut previous: i32 = window.iter().sum();

    while numbers.len() > 0 {
        window.pop_front();
        window.push_back(numbers.pop().expect("numbers empty even though it was checked"));

        let sum: i32 = window.iter().sum();

        if sum > previous {
            total += 1;
        }
        previous = sum;
    }

    return total;
}

fn main() {
    let content: String = fs::read_to_string("input.txt").expect("Reading input failed");

    println!("There are {} numbers higher than the previous",  part_a(&content));
    println!("There are {} sliding windows higher than the previous",  part_b(&content));
}
