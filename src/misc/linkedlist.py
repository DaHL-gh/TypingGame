from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Sequence, Union


@dataclass
class _Node:
    item: Any
    next: Optional[_Node] = None


class LinkedList:

    def __init__(self, items: Optional[Sequence] = None, first: Optional[_Node] = None) -> None:
        self._first = first
        self._length = 0

        if items:
            for item in items:
                self.append(item)

    def __iter__(self):
        if self._first is None:
            return iter([])

        self._curr = self._first
        return self

    def __next__(self):
        if self._curr is not None:
            t = self._curr
            self._curr = t.next
            return t.item
        else:
            raise StopIteration

    def append(self, item: Any) -> None:
        new_node = _Node(item)

        if self._first is None:
            self._first = new_node
        else:
            curr = self._first
            while curr.next is not None:
                curr = curr.next

            curr.next = new_node
        self._length += 1

    def __contains__(self, item: Any) -> bool:
        curr = self._first

        while curr is not None:
            if curr.item == item:
                return True

            curr = curr.next

        return False

    def __getitem__(self, i: Union[int, slice]) -> Union[Any, LinkedList]:

        if isinstance(i, int):

            if i < 0:
                i += self._length

            curr = self._first
            curr_index = 0

            while curr is not None and curr_index != i:
                curr = curr.next
                curr_index += 1

            if curr is None:
                raise IndexError
            else:
                return curr.item
        else:
            start = i.start
            stop = i.stop

            if start is None:
                start = 0
            if stop is None:
                stop = self._length

            if not (0 <= start <= stop <= len(self)):
                raise IndexError
            else:
                new_linked_list = LinkedList([])
                index = 0

                for item in self:
                    if start <= index < stop:
                        new_linked_list.append(item)
                    elif index > stop:
                        break
                    index += 1

                return new_linked_list

    def __len__(self) -> int:
        """Return the number of elements in this linked list.
        """
        return self._length

    def __eq__(self, other: LinkedList) -> bool:
        """Return whether this list and the other list are equal.
        """
        curr1 = self._first
        curr2 = other._first
        are_equal = True

        while are_equal and curr1 is not None and curr2 is not None:
            if curr1.item != curr2.item:
                are_equal = False
            curr1 = curr1.next
            curr2 = curr2.next

        return are_equal

    def __str__(self) -> str:
        """Return a string representation of this list.
        """
        return '[' + ' -> '.join([str(element) for element in self]) + ']'

    def __repr__(self) -> str:
        return f'LinkedList({self.__str__()})'

    def insert(self, i: int, item: Any) -> None:
        """Insert the given item at index i in this list.
        """
        if i < 0:
            i += self._length

        if i == 0:
            next_node = self._first
            self._first = _Node(item, next_node)
            self._length += 1
        else:
            curr = self._first
            curr_index = 0

            while curr is not None and curr_index != i - 1:
                curr_index += 1
                curr = curr.next

            if curr is None:
                raise IndexError
            else:
                new_node = _Node(item, curr.next)
                curr.next = new_node
                self._length += 1

    def pop(self, i: int) -> Any:
        """Remove and return the item at index i.
        """
        if i < 0:
            i += self._length

        if i == 0:
            if self._first:
                item = self._first.item
                self._first = self._first.next
                self._length -= 1
                return item
            else:
                raise IndexError
        else:
            curr = self._first
            curr_index = 0

            while curr is not None:
                if curr_index == i - 1:
                    if curr.next is None:
                        raise IndexError
                    else:
                        item = curr.next.item
                        curr.next = curr.next.next
                        self._length -= 1
                        return item

                curr = curr.next
                curr_index += 1
            raise IndexError

    def remove(self, item: Any) -> None:
        """Remove the first occurrence of item from the list.
        """
        curr = self._first

        if not curr:
            raise ValueError

        elif curr.item == item:
            self._first = self._first.next
            self._length -= 1

        else:
            while curr is not None:
                if curr.next and curr.next.item == item:
                    curr.next = curr.next.next
                    self._length -= 1
                    return
                curr = curr.next
            raise ValueError

    def count(self, item: Any) -> int:
        """Return the number of times the given item occurs in this list.
        """
        curr = self._first
        count = 0

        while curr is not None:
            if curr.item == item:
                count += 1
            curr = curr.next

        return count

    def index(self, item: Any) -> int:
        """Return the index of the first occurrence of the given item in this list.
        """
        index_so_far = 0
        curr = self._first

        while curr is not None:
            if curr.item == item:
                return index_so_far
            index_so_far += 1
            curr = curr.next
        raise ValueError

    def __setitem__(self, i: int, item: Any) -> None:
        """Store item at index i in this list.
        """
        if i < 0:
            i += self._length

        curr = self._first
        index_so_far = 0

        while curr is not None:
            if index_so_far == i:
                curr.item = item
                break
            index_so_far += 1
            curr = curr.next
        if curr is None:
            raise IndexError

    def invert(self) -> None:
        """Invert the linked list
        """

        curr = self._first
        previous = None

        while curr:
            curr_value = curr.next
            curr.next = previous

            previous = curr
            curr = curr_value

        self._first = previous

    def to_list(self) -> list:
        """Return a built-in Python list containing the items of this linked list.
        """
        items_so_far = []

        curr = self._first
        while curr is not None:
            items_so_far.append(curr.item)
            curr = curr.next

        return items_so_far

    def copy(self) -> LinkedList:
        return LinkedList(first=self._first)

    def extend(self, other: LinkedList) -> None:
        """Extend self by other linked list"""
        copy = self.copy()

        curr = other._first

        while curr is not None:
            copy.append(curr.item)
            curr = curr.next

        self._first = copy._first

    def __add__(self, other: LinkedList) -> LinkedList:
        copy = self.copy()

        curr = other._first

        while curr is not None:
            copy.append(curr.item)
            curr = curr.next

        return copy

    def sort(self, reverse: Optional[bool] = False):
        lst = self.to_list()
        lst.sort(reverse=reverse)
        copy = LinkedList(lst)
        self._first = copy._first
