'''
A great warm-up medium that uses arrays + prefix products (very common pattern) is:

LeetCode: 238. Product of Array Except Self (Medium)​

Given an integer array nums, return an array answer such that answer[i] is the product of all the elements of nums except nums[i].

The solution must run in O(n) time and without using division.

Example:

Input: nums = [1,2,3,4]
              [1,1,2,6]
              [6*4]
Output: [24,12,8,6]
'''
def productExceptSelf(nums):
    answers = [1] * len(nums)

    # find left multiples
    left_multiple = 1
    for i in range(len(nums)):
        answers[i] = left_multiple
        left_multiple = left_multiple * nums[i]
    
    #left : [1,1,2,6]
    
    #right: [1*1,1*2,2*4,6*1]
    right_multiple = 1
    # find right multiples
    for i in range(len(nums) - 1, -1, -1):
        print(i)
        answers[i] = answers[i] * right_multiple
        right_multiple = right_multiple * nums[i]
    
    return answers

print(productExceptSelf([1,2,3,4]))