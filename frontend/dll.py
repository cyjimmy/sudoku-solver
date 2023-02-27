class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return True if self.head is None else False

    def __len__(self):
        temp = self.head
        count = 0

        if not self.is_empty():
            while temp is not None:
                temp = temp.next
                count += 1
        return count

    def __contains__(self, data):
        temp = self.head
        contains = False

        if not self.is_empty():
            while temp is not None:
                if temp.data == data:
                    contains = True
                    break
                temp = temp.next
        return contains

    def get_node(self, data):
        temp = self.head
        if data in self:
            while temp is not None:
                if temp.data == data:
                    break
                temp = temp.next
        return temp

    def push(self, data):
        node = Node(data)

        if self.is_empty():
            self.head = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def append(self, data):
        node = Node(data)

        if self.is_empty():
            self.push(data)
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.next = node
            node.prev = temp

    def delete_from_last(self):
        if self.is_empty():
            print("Cannot delete elements from empty DLL.")
        elif self.head.next is None:
            self.head = None
        else:
            temp = self.head
            while temp.next is not None:
                temp = temp.next
            temp.prev.next = None
            temp.prev = None

    def delete(self, data):
        if self.is_empty():
            print("Cannot delete elements from empty DLL.")
        elif self.head.next is None:
            if self.head.data == data:
                self.head = None
        else:
            temp = self.head
            while temp is not None:
                if temp.data == data:
                    break
                temp = temp.next
            if temp is None:
                print("No such data value present!")
            elif temp.next is None:
                self.delete_from_last()
            else:
                temp.next = temp.prev.next
                temp.next.prev = temp.prev
                temp.next = None
                temp.prev = None

    def print(self):
        temp = self.head
        while temp is not None:
            print(temp.data)
            temp = temp.next

