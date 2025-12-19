'''The Challenge: Find the "Second Largest" Number Write a function second_largest(nums) that takes a list of integers and returns the second largest number in that list.

Example:

Input: [10, 20, 4, 45, 99]

Output: 45

Rules for this challenge:

Try to do it without using the built-in .sort() method.

Assume the list has at least two unique numbers.'''


def second_largest(my_list):
    # Initialize both to a very small value
    largest = float('-inf')
    second = float('-inf')

    for val in my_list:
        if val > largest:
            second = largest
            largest = val
        elif val != largest and val > second:
            second = val
            
    return second

nums = [10, 20, 15]
print(f"The second largest is: {second_largest(nums)}")