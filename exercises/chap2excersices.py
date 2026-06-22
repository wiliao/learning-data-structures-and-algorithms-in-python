class Flower():
    def __init__(self, name = "rose", petal_count = 5, price = 13.99):
        self._name = name
        self._petal_count = petal_count
        self._price = price
    
    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name

    def get_petal_count(self):
        return self._petal_count
    def set_petal_count(self, petal_count):
        self._petal_count = petal_count

    def get_price(self):
        return self._price
    def set_price(self, price):
        self._price = price

class CreditCard:
    '''A consumer credit card.'''

    def __init__(self, customer, bank, acnt, limit, balance = 0):
        '''Create a new credit card instance.

        The initial balance is zero.
        '''
        self._customer = customer
        self._bank = bank
        self._account = acnt
        self._limit = limit
        self._balance = balance

    def get_customer(self):
        '''Return name of the customer.'''
        return self._customer

    def get_bank(self):
        '''Return the bank's name.'''
        return self._bank

    def get_account(self):
        '''Return the card identifying number (typically stored as a string).'''
        return self._account

    def get_limit(self):
        '''Return current credit limit.'''
        return self._limit

    def get_balance(self):
        '''Return current balance.'''
        return self._balance
    
    def charge(self, price):
        '''Charge given price to the card, assuming sufficient credit limit.

        Return True if charge was processed; False if charge was denied.
        '''
        try:
            price = float(price)
            if price + self._balance > self._limit:  # if charge would exceed limit,
                return False  # cannot accept charge
            else:
                self._balance += price
                return True
        except ValueError:
            raise ValueError('price must be a number')

    def make_payment(self, amount):
        '''Process customer payment that reduces balance.'''
        if amount <= 0:
            raise ValueError('amount must be a positive number')
        self._balance -= amount

class Vector:
    """Represent a vector in a multidimensional space."""

    def __init__(self, d):
        """Create d-dimensional vector of zeros."""
        if isinstance(d, int) and d > 0:
            self._coords = [0] * d
        else:
            self._coords = []
            for i in d:
                self._coords.append(i)

    def __len__(self):
        """Return the dimension of the vector."""
        return len(self._coords)

    def __getitem__(self, j):
        """Return jth coordinate of vector."""
        return self._coords[j]

    def __setitem__(self, j, val):
        """Set jth coordinate of vector to given value."""
        self._coords[j] = val

    def __add__(self, other):
        """Return sum of two vectors."""
        if len(self) != len(other):  # relies on __len__ method
            raise ValueError('dimensions must agree')
        result = Vector(len(self))   # start with vector of zeros
        for j in range(len(self)):
            result[j] = self[j] + other[j]
        return result
    def __radd__(self, other):
        """Return sum of two vectors."""
        if len(self) != len(other):  # relies on __len__ method
            raise ValueError('dimensions must agree')
        result = Vector(len(self))   # start with vector of zeros
        for j in range(len(self)):
            result[j] = self[j] + other[j]
        return result
    
    def __sub__(self, other):
        """Return difference of two vectors."""
        if len(self) != len(other):  # relies on __len__ method
            raise ValueError('dimensions must agree')
        result = Vector(len(self))   # start with vector of zeros
        for j in range(len(self)):
            result[j] = self[j] - other[j]
        return result

    def __mul__(self, other):
        result = Vector(len(self))   # start with vector of zeros
        for j in range(len(self)):
            result[j] = self[j] * other
        return result

    def __neg__(self):
        result = Vector(len(self))   # start with vector of zeros
        for j in range(len(self)):
            result[j] = -self[j]
        return result

    def __eq__(self, other):
        """Return True if vector has same coordinates as other."""
        return self._coords == other._coords

    def __ne__(self, other):
        """Return True if vector differs from other."""
        return not self == other  # rely on existing __eq__ definition

    def __str__(self):
        """Produce string representation of vector."""
        return '<' + str(self._coords)[1:-1] + '>'  # adapt list representation

class Progression:
    """Iterator producing a generic progression.

    Default iterator produces the whole numbers 0, 1, 2, ...
    """

    def __init__(self, start=0):
        """Initialize current to the first value of the progression."""
        self._current = start

    def _advance(self):
        """Update self._current to a new value.

        This should be overridden by a subclass to customize progression.

        By convention, if current is set to None, this designates the
        end of a finite progression.
        """
        self._current += 1

    def __next__(self):
        """Return the next element, or else raise StopIteration error."""
        if self._current is None:    # our convention to end a progression
            raise StopIteration()
        else:
            answer = self._current   # record current value to return
            self._advance()          # advance to prepare for next time
            return answer            # return the answer

    def __iter__(self):
        """By convention, an iterator must return itself as an iterator."""
        return self

    def print_progression(self, n):
        """Print next n values of the progression."""
        print(' '.join(str(next(self)) for j in range(n)))

class FibonacciProgression(Progression):
    """Iterator producing a generalized Fibonacci progression."""

    def __init__(self, first=0, second=1):
        """Create a new fibonacci progression.

        first   the first term of the progression (default 0)
        second  the second term of the progression (default 1)
        """
        super().__init__(first)            # start progression at first
        self._prev = second - first        # fictitious value preceding the first

    def _advance(self):
        """Update current value by taking sum of previous two."""
        self._prev, self._current = self._current, self._prev + self._current

# prog = FibonacciProgression(2, 2)
# for i in range(7):
#     next(prog)
# print(prog._current)

from abc import ABCMeta, abstractmethod

class Sequence(metaclass=ABCMeta):
    """Our own version of collections.Sequence abstract base class."""

    @abstractmethod
    def __len__(self):
        """Return the length of the sequence."""
        pass

    @abstractmethod
    def __getitem__(self, j):
        """Return the element at index j of the sequence."""
        pass

    def __contains__(self, val):
        """Return True if val found in the sequence; False otherwise."""
        for j in range(len(self)):
            if self[j] == val:  # found match
                return True
        return False

    def index(self, val):
        """Return leftmost index at which val is found (or raise ValueError)."""
        for j in range(len(self)):
            if self[j] == val:  # leftmost match
                return j
        raise ValueError("value not in sequence")  # never found a match

    def count(self, val):
        """Return the number of elements equal to given value."""
        k = 0
        for j in range(len(self)):
            if self[j] == val:  # found a match
                k += 1
        return k

    def __eq__(self, other):
        try:
            if len(self) != len(other):
                return False
            for j in range(len(self)):
                if self[j] != other[j]:
                    return False
            return True
        except:
            return False
    
    def __lt__(self, other):
        for j in range(len(self)):
            try:
                if self[j] < other[j]:
                    return True
                elif self[j] > other[j]:
                    return False
            except IndexError:
                return False
        if len(self) < len(other):
            return True
        return False

