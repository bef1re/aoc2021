import cProfile

import torch
import torch.nn.functional as F

def step(img: torch.Tensor, trans: list[int], pad: int = 0) -> torch.Tensor:
    kernel = torch.tensor([[[
        [256, 128, 64],
        [32, 16, 8],
        [4, 2, 1]
    ]]])

    img = F.pad(img, (2, 2, 2, 2), value=pad)
    result = F.conv2d(img, kernel)

    new = torch.zeros_like(result)

    for i, val in enumerate(trans):
        new[result == i] = val

    return new

def run(img: torch.Tensor, trans: list[int], steps: int):
    for i in range(steps):
        pad = trans[-1] if i % 2 == 0 else trans[0]
        img = step(img, trans, pad)

    return img

def part_one(img, trans):
    return run(img, trans, steps=2).sum()

def part_two(img, trans):
    return run(img, trans, steps=50).sum()

def main():
    with open("day20/input.txt") as f:
        trans = [1 if c == "#" else 0 for c in f.readline()]
        f.readline()  # skip line
        img = torch.tensor([[1 if c == "#" else 0 for c in line] for line in f])

    img.unsqueeze_(0).unsqueeze_(0) # add batch and dimension channels

    print(f"The answer to part one is {part_one(img, trans)}")
    print(f"The answer to part two is {part_two(img, trans)}")

cProfile.run("main()", sort="cumtime")


"""
         666 function calls in 0.682 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.683    0.683 {built-in method builtins.exec}
        1    0.000    0.000    0.683    0.683 <string>:1(<module>)
        1    0.000    0.000    0.683    0.683 script.py:39(main)
        2    0.000    0.000    0.681    0.341 script.py:26(run)
       52    0.645    0.012    0.681    0.013 script.py:6(step)
        1    0.000    0.000    0.666    0.666 script.py:36(part_two)
       52    0.033    0.001    0.033    0.001 {built-in method conv2d}
        1    0.000    0.000    0.015    0.015 script.py:33(part_one)
       52    0.000    0.000    0.002    0.000 functional.py:4111(_pad)
       52    0.001    0.000    0.001    0.000 {built-in method constant_pad_nd}
       53    0.001    0.000    0.001    0.000 {built-in method tensor}
       52    0.001    0.000    0.001    0.000 {built-in method zeros_like}
        1    0.000    0.000    0.001    0.001 script.py:43(<listcomp>)
        2    0.000    0.000    0.000    0.000 {method 'sum' of 'torch._C._TensorBase' objects}
        1    0.000    0.000    0.000    0.000 {built-in method io.open}
        2    0.000    0.000    0.000    0.000 {built-in method builtins.print}
       52    0.000    0.000    0.000    0.000 _VF.py:25(__getattr__)
        2    0.000    0.000    0.000    0.000 {method 'unsqueeze_' of 'torch._C._TensorBase' objects}
        1    0.000    0.000    0.000    0.000 script.py:41(<listcomp>)
        2    0.000    0.000    0.000    0.000 {method 'readline' of '_io.TextIOWrapper' objects}
       54    0.000    0.000    0.000    0.000 {method 'dim' of 'torch._C._TensorBase' objects}
       52    0.000    0.000    0.000    0.000 {built-in method builtins.getattr}
        2    0.000    0.000    0.000    0.000 _tensor.py:567(__format__)
      104    0.000    0.000    0.000    0.000 {built-in method builtins.len}
       54    0.000    0.000    0.000    0.000 {built-in method torch._C._has_torch_function_unary}
        3    0.000    0.000    0.000    0.000 codecs.py:319(decode)
        2    0.000    0.000    0.000    0.000 {method 'item' of 'torch._C._TensorBase' objects}
        1    0.000    0.000    0.000    0.000 _bootlocale.py:33(getpreferredencoding)
        1    0.000    0.000    0.000    0.000 {method '__exit__' of '_io._IOBase' objects}
        1    0.000    0.000    0.000    0.000 codecs.py:309(__init__)
        3    0.000    0.000    0.000    0.000 {built-in method _codecs.utf_8_decode}
        2    0.000    0.000    0.000    0.000 {method '__format__' of 'int' objects}
        1    0.000    0.000    0.000    0.000 {built-in method _locale.nl_langinfo}
        1    0.000    0.000    0.000    0.000 codecs.py:260(__init__)
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
        1    0.000    0.000    0.000    0.000 codecs.py:331(getstate)
"""
