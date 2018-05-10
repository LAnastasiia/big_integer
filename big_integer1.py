# File: big_integer.py
# This module contains implementation of BigInteger and DigitNode classes.


class BigInteger:
    """
    Class for big integers, represented by double-linked list.
    Each digit is assigned to separate node.
    """
    def __init__(self, initValue="0"):
        # Reversed string of digits.
        self.initValue = str(initValue)[::-1]
        # Initialise head.
        self.head = DigitNode(self.initValue[0])
        self.head.prev = None
        self.tail = self.head
        self.tail.next = None

        for digit in self.initValue[1:]:
            newnode = DigitNode(digit)
            newnode.prev = self.tail
            self.tail.next = newnode
            self.tail = newnode
            self.tail.next = None

    def __str__(self):
        """
        Represent big integer as a string for printing it out.
        """
        res_str = ''
        node = self.tail
        while node is not None:
            res_str += str(node) + ' '
            node = node.prev
        return res_str

    def __repr__(self):
        """
        Represent big integer as string for vizualisation in collections.
        """
        return self.__str__()

    def __len__(self):
        """
        Get length of big integer.
        """
        node = self.head
        count = 0
        while node is not None:
            count += 1
            node = node.next
        return count

    def toString(self):
        """
        Return big integer as a string.
        """
        return self.__str__()

    def comparable(self, other):
        """
        Compare big integer with another big integer. This method is used for
        later implementation of <, <=, >, >=, ==, != operators.
        """
        if len(self) > len(other):
            return 1
        elif len(self) < len(other):
            return -1
        else:
            node1 = self.tail
            node2 = other.tail
            while node1 is not None:
                if node1.digit > node2.digit:
                    return 1
                elif node1.digit < node2.digit:
                    return -1
                else:
                    node1 = node1.prev
                    node2 = node2.prev
            return 0

    def __eq__(self, other):
        """
        Check if integers are equal.
        """
        if self.comparable(other) == 0:
            return True
        return False

    def __lt__(self, other):
        """
        Check if self is less than (<) other.
        """
        if self.comparable(other) == -1:
            return True
        return False

    def __le__(self, other):
        """
        Check if self is less than or equal to (<=) other.
        """
        if self.comparable(other) in {-1, 0}:
            return True
        return False

    def __gt__(self, other):
        """
        Check if self is greater than (<) other.
        """
        if self.comparable(other) == 1:
            return True
        return False

    def __ge__(self, other):
        """
        Check if self is greater than or equal to (>=) other.
        """
        if self.comparable(other) in {0, 1}:
            return True
        return False

    def __ne__(self, other):
        """
        Check if self is less not equal to (!=) other.
        """
        if self.comparable(other) != 0:
            return True
        return False

    def _add_to_structure(self, digit_node):
        """
        Append new DigitNode to the end of the big int.
        """
        if self.initValue == "0" and len(self) == 1:
            self.head = digit_node
            self.tail = self.head
            self.tail.next = None
            self.head.prev = None
            self.initValue = None
        else:
            digit_node.prev = self.tail
            self.tail.next = digit_node
            self.tail = digit_node
            self.tail.next = None

    def __add__(self, other):
        """
        Implementation of + operator for two big integers.
        """
        # Add 0-s to the beginning of smaller big integer.
        both_big_int = [self, other]
        longest = max(both_big_int, key=len)
        for bi in both_big_int:
            for _ in range(len(longest)-len(bi)):
                bi._add_to_structure(DigitNode(0))

        # Initialise node1 and node2.
        node1 = self.head
        node2 = other.head

        dec = 0  # Decimals (in case sum is >= 10).
        new_BigInt = BigInteger()

        while node1 is not None and node2 is not None:
            # Find sum of digits.
            digit_sum = node1.digit + node2.digit + dec

            if digit_sum >= 10:
                dec = digit_sum // 10
                digit_sum = digit_sum % 10
            else:
                dec = 0

            new_node = DigitNode(digit_sum)
            new_BigInt._add_to_structure(new_node)
            # Move to next nodes.
            node1 = node1.next
            node2 = node2.next

        if node1 is not None:
            while node1 is not None:
                new_BigInt._add_to_structure(node1)
                node1 = node1.next

        if node2 is not None:
            while node2 is not None:
                new_BigInt._add_to_structure(node2)
                node2 = node2.next
        if dec > 0:
            new_node = DigitNode(dec)
            new_BigInt._add_to_structure(new_node)
        return new_BigInt

    def __mul__(self, other):
        """
        Implementation of * operator for two big integers.
        """
        node1 = self.head
        res_list = []  # List for results of digit*big_int miltiplicatoin.
        count_fr_zero = 0
        res = BigInteger()  # Result.

        while node1 is not None:
            dec = 0
            new_BigInt = BigInteger()
            node2 = other.head

            while node2 is not None:
                mult_res = (node1.digit * node2.digit) + dec
                if mult_res >= 10:
                    dec = mult_res // 10
                    mult_res = mult_res % 10
                else:
                    dec = 0
                new_node = DigitNode(mult_res)
                new_BigInt._add_to_structure(new_node)
                node2 = node2.next

            if dec > 0:
                new_BigInt._add_to_structure(DigitNode(dec))
            for i in range(count_fr_zero):
                zero = DigitNode(0)
                new_BigInt._add_to_structure_front(zero)
            res_list.append(new_BigInt)
            node1 = node1.next
            count_fr_zero += 1

        for bi in res_list:
            res += bi
        return res

    def _add_to_structure_front(self, digit_node):
        """
        Helper method inserts digit_node on the beginning of structure.
        """
        digit_node.next = self.head
        self.head.prev = digit_node
        self.head = digit_node
        self.head.prev = None

    def __sub__(self, other):
        """
        Substraction method. Implementation of - operator for big integers.
        """
        if self < other:
            res = other.__sub__(self)
            minus_one = DigitNode(-1)
            minus = BigInteger()
            minus._add_to_structure(minus_one)
            res *= minus
            return res
        elif other == self:
            return 0
        else:
            # Add 0-s to the beginning of smaller big integer.
            both_big_int = [self, other]
            longest = max(both_big_int, key=len)
            for bi in both_big_int:
                for _ in range(len(longest)-len(bi)):
                    bi._add_to_structure(DigitNode(0))
            # Initialise node1 and node2.
            node1 = self.head
            node2 = other.head
            new_BigInt = BigInteger()

            while node1 is not None and node2 is not None:
                # Find sum of digits.
                digit_sub = node1.digit - node2.digit
                if digit_sub < 0 and node1.next is not None:
                    digit_sub = (node1.digit + 10) - node2.digit
                    next_node = node1.next  # For taking dec from next digit.
                    # If next digit is 0.
                    count = 0
                    while next_node == 0:
                        next_node.digit = 9
                        count += 1
                    # Take dec from next non-zero digit
                    next_node.digit -= 1

                new_node = DigitNode(digit_sub)
                new_BigInt._add_to_structure(new_node)
                # Move to next nodes.
                node1 = node1.next
                node2 = node2.next

            if node1 is not None:
                while node1 is not None:
                    new_BigInt._add_to_structure(node1)
                    node1 = node1.next

            if node2 is not None:
                while node2 is not None:
                    new_BigInt._add_to_structure(node2)
                    node2 = node2.next
            return new_BigInt

    def _fix_zeros(self):
        node = self.tail
        while node.digit == 0:
            self.tail = node.prev
            node = node.prev




class DigitNode:
    """
    Class for double-linked-lists's node which represents a single digit of
    BigInteger.
    """
    def __init__(self, digit):
        self.digit = int(digit)
        self.next = None
        self.prev = None

    def __str__(self):
        """
        Represent node for printing it out.
        """
        return str(self.digit)

    def __repr__(self):
        """
        Represent node in collections.
        """
        return str(self.digit)


bi = BigInteger('123')
b2 = BigInteger('11')
bi._fix_zeros()
print(bi)
