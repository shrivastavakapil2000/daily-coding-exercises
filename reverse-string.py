def reverse_string(s):
 old_str=""
 ans=""
 for i in s:
    print(i)
    ans = i+ old_str
    old_str = ans
 return ans

output = reverse_string('Hello')
print(f'outpiut:{output}')