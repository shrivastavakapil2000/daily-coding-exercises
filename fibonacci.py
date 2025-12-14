def fib(n):
    return n if n <= 1 else fib(n-1) + fib(n-2)

# Generate series
print([fib(i) for i in range(10)])        