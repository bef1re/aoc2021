use std::fs;
use std::collections::HashMap;

fn check_line(line: &str) -> (i32, Vec<char>) {
    let mut stack: Vec<char> = Vec::new();
    let mut symbols = HashMap::new();
    symbols.insert(')', ('(', 3));
    symbols.insert(']', ('[', 57));
    symbols.insert('}', ('{', 1197));
    symbols.insert('>', ('<', 25137));

    for c in line.chars() {
        if symbols.contains_key(&c) {
            let last = stack.pop().expect("stack empty");
            if last != symbols[&c].0 {
                stack.push(last);
                return (symbols[&c].1, stack);
            }
        } else {
            stack.push(c);
        }
    }
    (0, stack)
}

fn part_one(content: &String) -> i32 {
    let mut total = 0i32;

    for line in content.lines() {
        total += check_line(line).0;
    }

    total
}

fn part_two(content: &String) -> i64 {
    let openers = "([{<";
    let mut totals: Vec<i64> = Vec::new();

    for line in content.lines() {
        let mut total = 0i64;
        let (score, mut stack) = check_line(line);
        if score > 0 { continue; }
        stack.reverse();
        for c in stack {
            total *= 5;
            total += (openers.find(c).expect("Opener not in list") as i64) + 1;
        }
        totals.push(total);
    }
    totals.sort();
    totals[totals.len() / 2]
}

fn main() {
    let content: String = fs::read_to_string("input.txt").expect("Reading input failed");

    println!("The answer to part one is {}",  part_one(&content));
    println!("The answer to part two is {}",  part_two(&content));
}
