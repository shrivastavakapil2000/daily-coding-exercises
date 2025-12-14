def fibonacci(n):
    """
    Recursive function to calculate the nth Fibonacci number.
    
    Args:
        n (int): The position in the Fibonacci sequence (0-indexed)
        
    Returns:
        int: The nth Fibonacci number
    """
    # Base cases
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        # Recursive case: F(n) = F(n-1) + F(n-2)
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_series(count):
    """
    Generate a Fibonacci series of specified length using recursion.
    
    Args:
        count (int): Number of Fibonacci numbers to generate
        
    Returns:
        list: List containing the Fibonacci series
    """
    series = []
    for i in range(count):
        series.append(fibonacci(i))
    return series


# Example usage
if __name__ == "__main__":
    # Generate first 10 Fibonacci numbers
    n = 10
    print(f"First {n} Fibonacci numbers:")
    
    # Method 1: Using the series function
    fib_series = fibonacci_series(n)
    print(f"Series: {fib_series}")
    
    # Method 2: Individual calculations
    print("\nIndividual calculations:")
    for i in range(n):
        print(f"F({i}) = {fibonacci(i)}")        