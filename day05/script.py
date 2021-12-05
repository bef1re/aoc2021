import torch

"""
As you can read in the README, I'm using this Advent of Code to
experiment with new techniques and see when they work and when they don't.

This is an example of when the method does _not_ work.

The code is functional of course, but it's apparent that
tensors aren't the solution here
"""

def part_one(vent_list: torch.Tensor):
    size = vent_list.max().tolist() + 1
    map = torch.zeros((size, size), dtype=torch.int16)

    for vent in vent_list.tolist():
        # can I do an idiomatic computation instead?
        if (vent[0][0] != vent[1][0]) and (vent[0][1] != vent[1][1]):
            continue

        x = min(vent[0], vent[1])
        y = max(vent[0], vent[1])

        map[x[0]:y[0] + 1, x[1]:y[1] + 1] += 1

    # number of points where at least two overlap
    return map[map > 1].count_nonzero()

def part_two(vent_list: torch.Tensor):
    size = vent_list.max().tolist() + 1
    map = torch.zeros((size, size), dtype=torch.int16)

    for vent in vent_list.tolist():
        x = min(vent[0], vent[1])
        y = max(vent[0], vent[1])

        if (vent[0][0] == vent[1][0]) or (vent[0][1] == vent[1][1]):
            map[x[0]:y[0] + 1, x[1]:y[1] + 1] += 1
        else:
            """
            This part really shows this isn't the type of problem tensors should be used for 
            """
            line = torch.zeros_like(map, dtype=torch.bool)
            step0 = 1 if y[0] > x[0] else -1
            step1 = 1 if y[1] > x[1] else -1

            for i, j in zip(range(x[0], y[0] + step0, step0), range(x[1], y[1] + step1, step1)):
                line[i, j] = True

            map[line] += 1

    return map[map > 1].count_nonzero()

with open("day05/input.txt") as f:
    concatenated = f.read().replace(" -> ", " ").replace(","," ")
    vent_coords = [int(n) for n in concatenated.split()]

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
vent_list = torch.tensor(vent_coords, dtype=torch.int16, device=device)
vent_list = vent_list.reshape((-1, 2, 2))
print(vent_list)

print(f"The answer to part one is {part_one(vent_list)}")
print(f"The answer to part two is {part_two(vent_list)}")
