use std::fs;

fn part_one(content: &String) -> i32 {
    let mut xy = (0, 0);

    for line in content.lines() {
        let mut parts = line.split(" ");
        let command = parts.next().expect("Failed reading command");
        let speed: i32 = parts.next().expect("Failed reading amount").parse().unwrap();
        
        let direction = match command {
            "forward" => (1, 0),
            "down" => (0, 1),
            "up" => (0, -1),
            _ => panic!("Unexpected direction {}", command)
        };

        // Can I do something like numpy arrays can do in python?
        // xy += direction * speed;
        xy.0 += direction.0 * speed;
        xy.1 += direction.1 * speed;
    }
    
    xy.0 * xy.1
}

fn part_two(content: &String) -> i32 {
    let mut xy = (0, 0);
    let mut aim = 0;

    for line in content.lines() {
        let mut parts = line.split(" ");
        let command = parts.next().expect("Failed reading command");
        let speed: i32 = parts.next().expect("Failed reading amount").parse().unwrap();
        
        let direction = match command {
            "forward" => (1, aim, 0),
            "down" => (0, 0, 1),
            "up" => (0, 0, -1),
            _ => panic!("Unexpected direction {}", command)
        };

        xy.0 += direction.0 * speed;
        xy.1 += direction.1 * speed;
        aim += direction.2 * speed;
    }
    
    xy.0 * xy.1
}

fn main() {
    let content: String = fs::read_to_string("input.txt").expect("Reading input failed");

    println!("The solution to part one is {}",  part_one(&content));
    println!("The solution to part two is {}",  part_two(&content));
}
