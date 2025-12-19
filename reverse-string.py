def reverse_string(s):
    ans = ""
    for i in s:
        ans = i + ans  # Prepend the character to the current result
    return ans

output = reverse_string('Hello')
print(f'outpiut:{output}')