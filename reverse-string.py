def reverse_string(s):
    ans = ""
    for i in s:
        ans = i + ans  # Prepend the character to the current result
    return ans

output = reverse_string('Hello')
print(f'output:{output}')


# check if Palindrome
val_to_check="level"
assert(val_to_check == reverse_string(val_to_check))
print("Palindrome check passed!")