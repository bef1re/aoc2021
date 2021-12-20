import cProfile

import torch
import torch.nn.functional as F

kernel = torch.tensor([[[
    [256, 128, 64],
    [32, 16, 8],
    [4, 2, 1]
]]], dtype=torch.int32)


def step(img: torch.Tensor, ones: set[int], pad: int = 0) -> torch.Tensor:
    img = F.pad(img, (2, 2, 2, 2), value=pad)
    result = F.conv2d(img, kernel)

    new = torch.zeros_like(result, dtype=torch.bool)

    for n in ones:
        new.logical_xor_(result == n)

    return new.to(torch.int32)

def run(img: torch.Tensor, trans: list[int], steps: int):
    ones = {n for n, value in enumerate(trans) if value}

    for i in range(steps):
        pad = trans[-1] if i % 2 == 0 else trans[0]
        img = step(img, ones, pad)

    return img

def part_one(img, trans):
    return run(img, trans, steps=2).sum()

def part_two(img, trans):
    return run(img, trans, steps=50).sum()

def main():
    with open("day20/input.txt") as f:
        trans = [1 if c == "#" else 0 for c in f.readline()]
        f.readline()  # skip line
        img = torch.tensor([[1 if c == "#" else 0 for c in line] for line in f], dtype=torch.int32)

    img.unsqueeze_(0).unsqueeze_(0) # add batch and dimension channels

    print(f"The answer to part one is {part_one(img, trans)}")
    print(f"The answer to part two is {part_two(img, trans)}")

cProfile.run("main()", sort="cumtime")


"""
         15176 function calls in 0.367 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.367    0.367 {built-in method builtins.exec}
        1    0.000    0.000    0.367    0.367 <string>:1(<module>)
        1    0.000    0.000    0.367    0.367 script.py:39(main)
        2    0.000    0.000    0.366    0.183 script.py:24(run)
       52    0.219    0.004    0.365    0.007 script.py:13(step)
        1    0.000    0.000    0.357    0.357 script.py:36(part_two)
    14508    0.139    0.000    0.139    0.000 {method 'logical_xor_' of 'torch._C._TensorBase' objects}
        1    0.000    0.000    0.009    0.009 script.py:33(part_one)
       52    0.006    0.000    0.006    0.000 {built-in method conv2d}
       52    0.000    0.000    0.002    0.000 functional.py:4111(_pad)
       52    0.001    0.000    0.001    0.000 {built-in method constant_pad_nd}
        1    0.000    0.000    0.001    0.001 script.py:43(<listcomp>)
       52    0.000    0.000    0.000    0.000 {method 'to' of 'torch._C._TensorBase' objects}
       52    0.000    0.000    0.000    0.000 {built-in method zeros_like}
        1    0.000    0.000    0.000    0.000 {built-in method tensor}
        2    0.000    0.000    0.000    0.000 {method 'sum' of 'torch._C._TensorBase' objects}
        2    0.000    0.000    0.000    0.000 script.py:25(<setcomp>)
        1    0.000    0.000    0.000    0.000 {built-in method io.open}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
        2    0.000    0.000    0.000    0.000 {method 'unsqueeze_' of 'torch._C._TensorBase' objects}
       52    0.000    0.000    0.000    0.000 _VF.py:25(__getattr__)
        2    0.000    0.000    0.000    0.000 _tensor.py:567(__format__)
        1    0.000    0.000    0.000    0.000 script.py:41(<listcomp>)
        2    0.000    0.000    0.000    0.000 {method 'readline' of '_io.TextIOWrapper' objects}
        2    0.000    0.000    0.000    0.000 {method 'item' of 'torch._C._TensorBase' objects}
       52    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}
       54    0.000    0.000    0.000    0.000 {method 'dim' of 'torch._C._TensorBase' objects}
      104    0.000    0.000    0.000    0.000 {built-in method builtins.len}
       54    0.000    0.000    0.000    0.000 {built-in method torch._C._has_torch_function_unary}
        3    0.000    0.000    0.000    0.000 codecs.py:319(decode)
        1    0.000    0.000    0.000    0.000 _bootlocale.py:33(getpreferredencoding)
        3    0.000    0.000    0.000    0.000 {built-in method _codecs.utf_8_decode}
        1    0.000    0.000    0.000    0.000 {method '__exit__' of '_io._IOBase' objects}
        1    0.000    0.000    0.000    0.000 codecs.py:309(__init__)
        2    0.000    0.000    0.000    0.000 {method '__format__' of 'int' objects}
        1    0.000    0.000    0.000    0.000 {built-in method _locale.nl_langinfo}
        1    0.000    0.000    0.000    0.000 codecs.py:260(__init__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 codecs.py:331(getstate)
"""
