import time
import numpy as np

def f(x: int) -> int:
    return x**3 % 91

lst : list[int] = [i**2 % 91 for i in range(100000000)]

start = time.time()

gen_lst : list[int] = [f(x) for x in lst]

gen_sum = np.sum(gen_lst)

print(f'Gen time: {time.time() - start}.')

start = time.time()

map_lst = map(f, lst)

map_sum = np.sum(map_lst)

print(f'Map time: {time.time() - start}.')

print(gen_sum, map_sum)