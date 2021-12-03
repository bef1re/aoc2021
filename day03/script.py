import torch

def binary_tensor_to_int(inp):
    """ Convert tensor of Trues and Falses to int """
    result = inp.flip(dims=(0, )).tolist()
    return sum([n * 2 ** i for i, n in enumerate(result)])


def part_one(numbers):
    # Get the most common values per column
    modes = numbers.mode(dim=0).values

    gamma = binary_tensor_to_int(modes)
    epsilon = binary_tensor_to_int(modes.logical_not())

    return gamma * epsilon


def part_two(numbers):
    def find(matches, invert=False):
        for i in range(matches.size(dim=1)):
            # Calculate the mode ourself, to be sure about tiebreakers
            mode = matches[:, i].sum() / matches.size(dim=0) >= 0.5

            mode ^= invert  # support carbon

            if mode:
                match_indices = matches[:, i].nonzero()
            else:
                match_indices = matches[:, i].logical_not().nonzero()
 
            matches = matches[match_indices].squeeze()

            # If we got squeezed to 1 dimension,
            # that means there was only one left
            if matches.dim() == 1:
                break
                
        assert matches.dim() == 1, f"Found multiple matches"
        return matches


    oxygen = find(numbers)
    carbon = find(numbers, invert=True)

    return binary_tensor_to_int(oxygen) * binary_tensor_to_int(carbon)


# Read the file to an array of bools
with open("input.txt") as f:
    content = [[bool(int(n)) for n in line.strip()] for line in f.readlines()]

# Move to the GPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
numbers = torch.tensor(content, device=device)

# Evaluate
print(f"The answer to part one is {part_one(numbers)}")
print(f"The answer to part two is {part_two(numbers)}")
