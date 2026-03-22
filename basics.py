## Variables and Data Types

# Integer 
X = 5 
print(f"Integer: {X}")

# Float
Y = 3.14
print(f"Float: {Y}")

# String
name = "Alice"
print(f"String: {name}")

#List 
numbers = [1, 2, 3, 4, 5]
print(f"List: {numbers}")

# Tuple
point = (2, 3)
print(f"Tuple: {point}")

# Dictionary
person = {"name": "Alice", "age": 25}
print(f"Dictionary: {person}")

## Basic Operations 

# Arithmetic Operations
a = 10+5 
b = 10-5
c = 10*5
d = 10/5

print(f"Addition: {a}")
print(f"Subtraction: {b}")
print(f"Multiplication: {c}")
print(f"Division: {d}")

# String Manipulation
greeting = "Hello"
greeting = greeting + ", World!"
print(f"String Concatenation: {greeting}")

## Control Structures
x = 10
if x > 0:
    print("x is positive")
else:   
    print("x is negative")

## Loops
# For Loop
for i in range(5):
    print(f"For Loop Iteration: {i}")

# While Loop
print("While Loop:")
i = 0
while i < 5:
    print(f"While Loop Iteration: {i}")
    i += 1

## Functions
def add(a, b):
    return a + b

result = add(5, 3)
print(f"Function Result: {result}")