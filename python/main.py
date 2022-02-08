# fibonacci
from fibonacci import fibIter, fibRec
fib_input = 46
print(fibIter(fib_input))
print(fibRec(fib_input))

# merge sort
from merge_sort import merge_sort
from numpy import random
array = random.randint(10000)
merge_sort(array)
