# Ethan Palmisano
# MET-330
# This is a script with a bunch of examples of for loops.

# Example 1: What does a for loop do?
print('Example 1: for letter in letters')
letters = ['a','b','c']
for letter in letters:
	print(letter)

# Example 2: Looping Over a Range
print('Example 2: for i in range')
for i in range(len(letters)):
	print(i)

# Example 3: Looping Over Multiple Variables at Once
print('Example 3: for l, n, in letters, numbers')
numbers = [1,2,3,4]
for (l, n) in zip(letters, numbers):
	print(l,n)

# Example 4: Enumerate
print('Example 4: Enumerate')
for i, letter in enumerate(letters):
	print(i, letter)

# Example 5: Nested Loops
print('Example 5: for i in list: for j in list:')
for i in range(5):
	for j in range(4):
		print(f'{i} * {j} = {i*j}')
		i = i**(j+1)
	print(f'i is {i}')
