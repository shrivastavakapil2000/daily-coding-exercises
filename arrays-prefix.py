'''
A great warm-up medium that uses arrays + prefix products (very common pattern) is:

LeetCode: 238. Product of Array Except Self (Medium)​

Given an integer array nums, return an array answer such that answer[i] is the product of all the elements of nums except nums[i].

The solution must run in O(n) time and without using division.

Example:

Input: nums = [1,2,3,4]

Output: [24,12,8,6]
'''


def productExceptSelf(nums):
    n = len(nums)
    answer = [1] * n

    # 1) Left products
    left_product = 1
    for i in range(n):
        answer[i] = left_product
        left_product = left_product * nums[i]

    # 2) Right products
    right_product = 1
    for i in range(n - 1, -1, -1):
        answer[i] = answer[i] * right_product
        right_product = right_product * nums[i]

    return answer

print(productExceptSelf([1,2,3,4]))