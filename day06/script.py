def run(lf, iterations):
    lf += lf[:2]  # 7, 8 are the same as 0, 1

    for i in range(9, iterations + 9):  # add 9 more, because we're only counting the newborns
        lf.append(lf[i - 9] + lf[i - 7])

    return sum(lf[-7:])  # the sum of the last 7 elements equals the population at -9

lanternfish = [0] * 7
with open("day06/input.txt") as f:
    for item in f.read().split(","):
        lanternfish[int(item)] += 1

print(f"The answer to part one is {run(lanternfish.copy(), 80)}")
print(f"The answer to part two is {run(lanternfish.copy(), 256)}")
