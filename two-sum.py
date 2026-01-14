def two_sum(nums, target):
    """
    Given an array of integers nums and an integer target,
    return indices of the two numbers such that they add up to target.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    # Dictionary to store number and its index
    seen = {}
    
    for i, num in enumerate(nums):
        # Calculate what number we need to find
        complement = target - num
        
        # Check if we've seen the complement before
        if complement in seen:
            return [seen[complement], i]
        
        # Store current number and its index
        seen[num] = i
    
    # No solution found
    return []

# Test cases
print("Two Sum Problem - Find indices of two numbers that add up to target")
print("-" * 60)

# Test 1
nums1 = [2, 7, 11, 15]
target1 = 9
result1 = two_sum(nums1, target1)
print(f"Input: nums = {nums1}, target = {target1}")
print(f"Output: {result1}")
if result1:
    print(f"Explanation: nums[{result1[0]}] + nums[{result1[1]}] = {nums1[result1[0]]} + {nums1[result1[1]]} = {target1}")
else:
    print("Explanation: No solution found")
print()

# Test 2
nums2 = [3, 2, 4]
target2 = 6
result2 = two_sum(nums2, target2)
print(f"Input: nums = {nums2}, target = {target2}")
print(f"Output: {result2}")
if result2:
    print(f"Explanation: nums[{result2[0]}] + nums[{result2[1]}] = {nums2[result2[0]]} + {nums2[result2[1]]} = {target2}")
else:
    print("Explanation: No solution found")
print()

# Test 3
nums3 = [3, 3]
target3 = 6
result3 = two_sum(nums3, target3)
print(f"Input: nums = {nums3}, target = {target3}")
print(f"Output: {result3}")
if result3:
    print(f"Explanation: nums[{result3[0]}] + nums[{result3[1]}] = {nums3[result3[0]]} + {nums3[result3[1]]} = {target3}")
else:
    print("Explanation: No solution found")
