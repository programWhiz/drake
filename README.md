# Drake

## Manifesto

Code should be opionated, without flexibility to express the same idea
in a myriad of ways through obscure syntax.

Code should be as simple as possible, but no simpler.

Code should be elegant, idioms which occur most frequently should be easiest to express.
Boilerplate should be exterminated.

Most code should be loosely specified, the compiler should optimize. 
Performance intensive or library code should have the ability to be more rigorous.

Compiled is better than interpreted.

The language should be easy to type.

## Langugae Features

Fully compiled into native assembly.

REPL interface for interactive testing.

Easy syntax and format (Python-like)

Types and memory management are all inferred from the code itself.  The ability
to explicitly declare types is preserved.

## Syntax

### Object oriented style:

```
class Animal:
    # Declare instance variables, and default constructor values
    height = 3.0
    length = 4.5
    weight = 2.0
    fur = False

    def has_fur():
        # Refers to instance variable "fur"
        return fur

    
       
# At construction, create a new instance and set some instance attributes 
a = Animal(height=3.14, length=10.1)
```

### Functional style:
Functions are declared using either a return type, or the keyword `fn` to use an implied return type.
Function bodies consist of an indented set of lines
```
fn foo(n):
    print(n)
```

### Flow Control
Standard if / else syntax, with keyword elif for "else if" blocks:
```
if x > 3:
  y += 4
elif x > 10:
  y += 6
else:
  y += 8
```

### Loops

For loops iterate over iterators:
```
for i in range(10, 100):
   print(i)
```

While loops allow full loop control:
```
i = 0
while i < 100:
   print(i)
   i += 1
```

The "do once" means the loop body executes once before checking the exit condition:
```
i = 0
do while i < 100:
   print(i)
   i += 1
```

The keyword "break" exits the loop, and "continue" jumps back to the loop start:
```
for i in range(100):
   if i % 10 == 0:
     break  # stop at i == 10
   if i % 3 == 0:
     continue   # restart when i in (0, 3, 6, 9)
   print(i)

=> 1, 2, 4, 5, 7, 8
``` 

### Data structures:
```
# declare a collection of items
x = [ 1, 2, 3 ]
# declare a key/value collection of items
x = { "a": 1, "b": 3.5 }
```

These builtin data structures are supported:

**list** an ordered, dynamically growing array of items

**tuple** an ordered, fixed size collection of items.

**set** an unordered, dynamic collection of items with O(1) lookup

**dict** an unordered key value pair store with O(1) lookup

### Comprehensions:
```
# A list comprehension
x = [ item for item in items if cond(item) ]
# A set comprehension
x = set( item for item in items if cond(item) )
# A dictionary comprehension
x = { item.key: item.value for item in items if cond(item) }
```

### Type hints:
The type of a variable can be specified at various levels of detail:
```
x = 3    # will choose default integer type
int x = 3    # specify default integer type
int32 x = 3  # specify specific precision of integer
```

### Type hints for collections:
The type of a collection can be fully inferred, or specified to different levels of precision.
```
x = [ 1, 2, 3 ]   # x is a collection, list of integers is implied
set y = [ 1, 2, 3 ]     # y is a set, integers is implied
set<int> z              # z is a set of integers
set<int32> w            # w is a set of 32-bit integers
set<int32|str> u        # u is a set of 32-bit integers or strings
set<set<int32|str>> v   # v is a set of sets of 32-bit integers or strings
dict<int32|str, float> v   # v is a dictionary with keys that can be integers or strings, and values that must be floats
```

### Type hints for classes:
For objects of a class type, if no hint is given, the most specific
version of the classes instantiated is used.

```
class Parent:
    pass

class Child(Parent):
    pass

# My default, my_inst1 is assumed to be of type "Child", since
# type "Parent" is never assigned to my_inst1
my_inst1 = Child()

# This is not an error, my_inst2 will have inferred type "Parent" since
# it has been assigned both types
my_inst2 = Child()
my_inst2 = Parent()

# This will be an error, y can only be subclass "Child"
Child my_inst3 = Parent()
```

### Storage and mutability

#### const readonly values
Items marked with "const" are readonly
```
const pi = 3.1415

# This is an error
pi += 2.0
```

#### nullable and not-nullable
By default, any variables could take on a null value `none`.
The "!" operator makes a value non-nullable.  This will cause an error if none is ever assigned.
The "!" is placed immediately after the declaration of the variable name.
```
!x = 3              # x is an integer that can never be null
x  = none           # ERROR! x can never be assigned none
int32 ! y = 4       # y must be a 32-bit integer, and can never be none
```
