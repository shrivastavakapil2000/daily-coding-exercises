def fibonacci(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

def print_fibonacci_series(count, current=0):
    # Base case: stop when we've printed enough numbers
    if current >= count:
        return
    
    # Print current fibonacci number
    print(fibonacci(current), end=" ")
    
    # Recursive call for next number
    print_fibonacci_series(count, current + 1)

# Print first 10 fibonacci numbers
print("Fibonacci series:")
print_fibonacci_series(10)
print()  # New line at the end