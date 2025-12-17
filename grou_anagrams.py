'''Given an array of strings strs, group the anagrams together. You can return the answer in any order.
Example: * Input: 
strs = ["eat","tea","tan","ate","nat","bat"]
Output:[["bat"],["nat","tan"],["ate","eat","tea"]]'''



class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseList(head):
    prev = None
    curr = head
    
    while curr:
        nxt = curr.next  # Temporarily store next node
        curr.next = prev # Reverse the link
        prev = curr      # Move prev to current
        curr = nxt       # Move current to next
        
    return prev