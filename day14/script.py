import torch
import cProfile

def build_transition_matrix(grammar):
    result = torch.zeros(len(grammar), len(grammar), dtype=torch.int64)
    for x, key in enumerate(grammar):
        for value in grammar[key]:
            y = list(grammar).index(value)
            result[x, y] = 1

    return result

def build_letter_mapping(grammar):
    result = torch.zeros(len(grammar), 26, dtype=torch.int64)
    for x, key in enumerate(grammar):
        for letter in key:
            y = ord(letter) - ord("A")  # y = position in uppercase alphabet
            result[x, y] += 1

    return result

def build_word_vector(grammar, word):
    result = torch.zeros(len(grammar), dtype=torch.int64)
    for i in range(len(word) - 1):
        x = list(grammar).index(word[i:i+2])
        result[x] += 1

    return result

def calculate(grammar, template, n):
    trans = build_transition_matrix(grammar)
    lettermap = build_letter_mapping(grammar)
    word = build_word_vector(grammar, template)

    trans = trans.matrix_power(n)  # Calculate the transition matrix after n iterations
    result = (trans.T * word).sum(dim = 1)  # Apply the transition matrix to our word
    result = (result * lettermap.T).sum(dim = 1)  # Result is in two-letter symbols, map it back to letters

    # Everything is duplicate, except the first and last letters
    # It happens to be the case that the first and last are the only odd numbers here
    # so we want to do a ceiling division, except we can't, so we do this:
    result += 1
    result.div_(2, rounding_mode="trunc")

    return result.max() - result[result > 0].min()

def part_one(grammar, template):
    return calculate(grammar, template, 10)

def part_two(grammar, template):
    return calculate(grammar, template, 40)

def read_data(filename):
    with open("day14/input.txt") as f:
        template = f.readline().strip()
        f.readline()  # skip newline
        grammar = {}
        for line in f:
            key, value = line.strip().split(" -> ")
            grammar[key] = [key[0] + value, value + key[1]]
    return grammar, template


def main():
    grammar, template = read_data("day14/input.txt")

    print(f"The answer to part one is {part_one(grammar, template)}")
    print(f"The answer to part two is {part_two(grammar, template)}")

cProfile.run("main()", sort="cumtime")


""" Output: 

The answer to part one is ####
The answer to part two is #############

         1507 function calls in 0.025 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.025    0.025 {built-in method builtins.exec}
        1    0.000    0.000    0.025    0.025 <string>:1(<module>)
        1    0.000    0.000    0.025    0.025 script.py:63(main)
        2    0.000    0.000    0.024    0.012 script.py:29(calculate)
        2    0.019    0.009    0.019    0.009 {method 'matrix_power' of 'torch._C._TensorBase' objects}
        1    0.000    0.000    0.014    0.014 script.py:49(part_two)
        1    0.000    0.000    0.010    0.010 script.py:46(part_one)
        2    0.002    0.001    0.002    0.001 script.py:12(build_letter_mapping)
        2    0.002    0.001    0.002    0.001 script.py:3(build_transition_matrix)
        2    0.000    0.000    0.000    0.000 {method 'max' of 'torch._C._TensorBase' objects}
      438    0.000    0.000    0.000    0.000 {method 'index' of 'list' objects}
        2    0.000    0.000    0.000    0.000 script.py:21(build_word_vector)
        6    0.000    0.000    0.000    0.000 {built-in method zeros}
        1    0.000    0.000    0.000    0.000 script.py:52(read_data)
        4    0.000    0.000    0.000    0.000 {method 'sum' of 'torch._C._TensorBase' objects}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        1    0.000    0.000    0.000    0.000 {built-in method io.open}
        2    0.000    0.000    0.000    0.000 _tensor.py:567(__format__)
      800    0.000    0.000    0.000    0.000 {built-in method builtins.ord}
        2    0.000    0.000    0.000    0.000 {method 'min' of 'torch._C._TensorBase' objects}
        2    0.000    0.000    0.000    0.000 {method 'div_' of 'torch._C._TensorBase' objects}
        2    0.000    0.000    0.000    0.000 {method 'item' of 'torch._C._TensorBase' objects}
        2    0.000    0.000    0.000    0.000 {method 'readline' of '_io.TextIOWrapper' objects}
      100    0.000    0.000    0.000    0.000 {method 'split' of 'str' objects}
      101    0.000    0.000    0.000    0.000 {method 'strip' of 'str' objects}
        1    0.000    0.000    0.000    0.000 _bootlocale.py:33(getpreferredencoding)
        2    0.000    0.000    0.000    0.000 codecs.py:319(decode)
        2    0.000    0.000    0.000    0.000 {method 'dim' of 'torch._C._TensorBase' objects}
        1    0.000    0.000    0.000    0.000 codecs.py:309(__init__)
        2    0.000    0.000    0.000    0.000 {method '__format__' of 'int' objects}
        1    0.000    0.000    0.000    0.000 {method '__exit__' of '_io._IOBase' objects}
        1    0.000    0.000    0.000    0.000 {built-in method _locale.nl_langinfo}
       10    0.000    0.000    0.000    0.000 {built-in method builtins.len}
        2    0.000    0.000    0.000    0.000 {built-in method _codecs.utf_8_decode}
        2    0.000    0.000    0.000    0.000 {built-in method torch._C._has_torch_function_unary}
        1    0.000    0.000    0.000    0.000 codecs.py:260(__init__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 codecs.py:331(getstate)
"""
