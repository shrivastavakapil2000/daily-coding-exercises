def fibonacci(n):
    print(f'function got called:{n}')
    # Base cases: first two numbers in sequence
    if n == 0:        
        return 0
    if n == 1:
        return 1
    
    # Recursive case: sum of previous two numbers
    return fibonacci(n - 1) + fibonacci(n - 2)

# Test the function
print("Fibonacci numbers:")
for i in range(8):
    print(f"F({i}) = {fibonacci(i)}")        