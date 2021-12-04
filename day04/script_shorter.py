import torch

def remaining(boards: torch.Tensor):
    """ Count how close to a bingo a board is """
    x_remaining = boards.count_nonzero(dim=1).min(dim=1).values
    y_remaining = boards.count_nonzero(dim=2).min(dim=1).values
    return x_remaining.minimum(y_remaining)


def score(number: int, board: torch.Tensor):
    """ Count the score, and undo the offset """
    score = board.sum() - (board != 0).count_nonzero()
    return score * number


def part_one(numbers: list[int], boards: torch.Tensor):
    for number in numbers:
        boards[boards == number + 1] = 0  # Zero out the drawn number

        winners = (remaining(boards) == 0).nonzero()

        if len(winners):
            return score(number, boards[winners.squeeze()])


def part_two(numbers: list[int], boards: torch.Tensor):
    for number in numbers:
        boards[boards == number + 1] = 0

        non_winners = (remaining(boards) != 0).nonzero()

        if len(non_winners) == 1:
            last_board = non_winners.squeeze().tolist()
        elif len(non_winners) == 0:
            return score(number, boards[last_board])


with open("day04/input.txt") as f:
    numbers = [int(n) for n in f.readline().strip().split(",")]
    fields = [int(n) + 1 for n in f.read().split()]  # Offset so we can use 0

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
boards = torch.tensor(fields, dtype=torch.int8, device=device)
boards = boards.reshape((-1, 5, 5))

print(f"The answer to part one is {part_one(numbers, boards.detach().clone())}")
print(f"The answer to part two is {part_two(numbers, boards)}")
