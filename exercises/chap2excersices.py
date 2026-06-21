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
        self._coords = [0] * d

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

u = Vector(3)
v = Vector(3)
u[0] = 1
u[1] = 2
u[2] = 3
v[0], v[1], v[2] = 4, 5, 6
print(u * 134)