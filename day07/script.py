import pandas as pd
import numpy as np

def score(number):
    """
    The score in part two is the 'sum of the first n numbers',
    which can be calculated directly
    """
    return 0.5 * number * (number + 1)


def part_two(crabs):
    cheapest = np.inf

    for potential in crabs:
        sc = sum([score(abs(crab - potential)) for crab in crabs])
        if sc < cheapest:
            cheapest = sc

    return cheapest


def part_one(crabs):
    """
    The most efficient position for the crabs to go to, is the median
    So we calculate the sum of the absolute differences with the median
    """
    crabs -= crabs.median()
    return sum(crabs.abs())


with open("day07/input.txt") as f:
    data = [int(n) for n in f.read().split(",")]
    crabs = pd.Series(data).sort_values()

print(f"The answer to part one is {part_one(crabs.copy())}")
print(f"The answer to part two is {part_two(crabs.copy())}")
