import torch


def part_one(numbers: list[int], boards: torch.Tensor):
    skip_checks = 4  # We don't need to check the first four placements
    for number in numbers:
        # Zero out the drawn number
        boards[boards==number+1] = 0

        # No need to check if we know we're not gonna find a match
        if skip_checks:
            skip_checks -= 1
            continue

        # Count how close we are to a bingo
        x_remaining = boards.count_nonzero(dim=1).min(dim=1).values
        y_remaining = boards.count_nonzero(dim=2).min(dim=1).values
        remaining = x_remaining.minimum(y_remaining)

        # winners now contains the index of where remaining==0 is True
        winners = (remaining==0).nonzero()

        if len(winners) > 0:
            # Winner found, sum everything up and multiply current number
            winner = winners.squeeze().tolist()
            score = boards[winner].sum() 

            # Undo the +1's we did to free up the 0
            score -= (boards[winner] != 0).count_nonzero()
            return score * number

        # tolist() is called list but the tensor is 0-dimensional
        # so we get an int instead
        skip = remaining.min().tolist() - 1
        
    return boards


def part_two(numbers: list[int], boards: torch.Tensor):
    skip_checks = 4
    last_board = None

    for number in numbers:
        boards[boards==number+1] = 0

        if skip_checks:
            skip_checks -= 1
            continue

        x_remaining = boards.count_nonzero(dim=1).min(dim=1).values
        y_remaining = boards.count_nonzero(dim=2).min(dim=1).values
        remaining = x_remaining.minimum(y_remaining)

        # Check non_winners instead of winners
        non_winners = (remaining!=0).nonzero()
        if len(non_winners) == 1:
            # Remember who the last one was
            last_board = non_winners.squeeze().tolist()

        if len(non_winners) == 0:
            assert last_board, "Multiple boards won last"

            score = boards[last_board].sum() 
            score -= (boards[last_board] != 0).count_nonzero()
            return score * number

        # We can skip even more now
        # taking the max from remaining instead of the min
        skip = remaining.max().tolist() - 1
        
    return boards


with open("day04/input.txt") as f:
    # Read drawn numbers from the first line.
    # We reverse it, because .pop(0) is O(n) and .pop() is O(1)
    numbers = [int(n) for n in f.readline().strip().split(",")]

    # Skip empty line in between 
    f.readline()

    # Get all lines so we know the size
    lines = f.readlines()
    boards = []

    # Go in groups of 6 lines (5 + empty line)
    for i in range(0, len(lines), 6):  
        # Increment every number by 1, because we want to use the 0 ourself
        new_board = [[int(n) + 1 for n in line.split()] for line in lines[i:i+5]]
        boards.append(new_board)

    print(boards)


# Use GPU if available
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
boards = torch.tensor(boards, dtype=torch.int8, device=device)
print(boards)

# Evaluate
print(f"The answer to part one is {part_one(numbers, boards.detach().clone())}")
print(f"The answer to part two is {part_two(numbers, boards)}")
