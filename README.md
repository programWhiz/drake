# Drake

## Syntax

Object oriented style:

```
class Animal:
    def __init__(self, height, weight, fur):
        self.height = height
        self.weight = weight
        self.fur = fur

a = Animal(3.14, 10.1, True)
```

Functional style:
```
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

def combos(n, k):
    return factorial(n) / (factorial(n - k) * factorial(k))

n_combos = combos(10, 3)
print(n_combos)
```
