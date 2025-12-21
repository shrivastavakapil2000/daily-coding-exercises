def moveZeroes(nums):
    k = 0  # position to put next non-zero

    for i in range(len(nums)):
        if nums[i] != 0:
            # Only swap when i and k are different to avoid useless swaps
            if i != k:
                nums[i], nums[k] = nums[k], nums[i]
            k += 1


# Example usage:
nums1 = [0, 1, 0, 3, 12]
moveZeroes(nums1)
print(nums1)  # [1, 3, 12, 0, 0]

nums2 = [0]
moveZeroes(nums2)
print(nums2)  # [0]

nums3 = [1, 2, 3]
moveZeroes(nums3)
print(nums3)  # [1, 2, 3]
