class Node(object):
    def __init__(self, data):
        self._data = data
        self._next = None

class LinkedList(object):
    def __init__(self):
        self._head = None

    def print_list(self):
        temp = self._head
        while(temp):
            print(temp._data)
            temp = temp._next

    def insert_at_beginning(self,data):
        node = Node(data)

        node._next = self._head
        self._head = node

    def insert_in_between(self, middle_node, data):
        node = Node(data)
        temp = self._head
        while(temp._next):
            if(temp._data == middle_node):
                node._next = temp._next
                temp._next = node
                return
            temp = temp._next
        else:
            print("Node is not present")


    def insert_in_end(self, data):
        node = Node(data)

        if self._head is None:
            self._head = node
            return

        last = self._head
        while(last._next):
            last = last._next
        last._next = node

    def delete_node(self, data):
        prev = None
        head_val = self._head

        if head_val is not None:
            if head_val._data == data:
                self._head = head_val._next
                head_val = None
                return
        while head_val is not None:
            if head_val._data == data:
                break
            prev = head_val
            head_val = head_val._next

        if head_val == None:
            return

        prev._next = head_val._next
        head_val = None



llist = LinkedList()
llist._head = Node(1)
second = Node(2)
third = Node(4)

llist._head._next = second
second._next = third
llist.insert_at_beginning(0)
llist.insert_in_between(2,3)
llist.delete_node(4)

llist.print_list()

