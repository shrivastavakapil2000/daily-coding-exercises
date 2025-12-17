'''
Given the head of a singly linked list, reverse the list, and return the reversed list.
Example:
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]
'''
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# --- Helper Functions for Testing ---
def create_linked_list(arr):
    """Converts a Python list to a Linked List."""
    if not arr:
        return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def linked_list_to_list(head):
    """Converts a Linked List back to a Python list for easy assertion."""
    result = []
    curr = head
    while curr:
        result.append(curr.val)
        curr = curr.next
    return result

# --- The Function to Test ---

def reverseList(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev

# --- The Test Function ---

def test_reverse():
    # Case 1: Standard list
    input_arr = [1, 2, 3, 4, 5]
    head = create_linked_list(input_arr)
    reversed_head = reverseList(head)
    assert linked_list_to_list(reversed_head) == [5, 4, 3, 2, 1]
    
    # Case 2: Single element
    head = create_linked_list([1])
    reversed_head = reverseList(head)
    assert linked_list_to_list(reversed_head) == [1]
    
    # Case 3: Empty list
    head = create_linked_list([])
    reversed_head = reverseList(head)
    assert linked_list_to_list(reversed_head) == []
    
    print("All tests passed! ✅")

# Run the test
if __name__ == "__main__":
    test_reverse()

