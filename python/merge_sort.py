# option 1
from heapq import merge
 
def merge_sort(m):
    if len(m) <= 1:
        return m
 
    middle = len(m) // 2
    left = m[:middle]
    right = m[middle:]
 
    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge(left, right))

# option 2 - using only recursions
def merge(x, y):
    if x==[]: return y
    if y==[]: return x
    return [x[0]] + merge(x[1:], y) if x[0]<y[0] else [y[0]] + merge(x, y[1:])
 
def sort(a, n):
    m = n//2
    return a if n<=1 else merge(sort(a[:m], m), sort(a[m:], n-m))
 
a = list(map(int, input().split()))
print(sort(a, len(a)))