def is_multiple(n, m):
    if n % m == 0:
        print(True)
    else:
        print(False)

def is_even(k):
    if k > 0:
        while k > 0:
            k = k - 2
        if k == 0:
            print(True)
        else:
            print(False)
    elif k < 0:
        while k < 0:
            k = k + 2
        if k == 0:
            print(True)
        else:
            print(False)
    else:
        print(True)

def thingy(n):
    su = sum([n ** 2 for n in range(n)])
    return su

def odd_square_sum(n):
    sum = 0
    for i in range(n):
        if i % 2 == 1:
            sum = sum + i ** 2
    return sum

def odd_square_sum2(n):
    su = sum([n ** 2 for n in range(n) if n % 2 == 1])
    return su

def tens_yielder():
    return list(range(8, -10, -2))

def squares():
    return [2 ** n for n in range(9)]

seq = [1, 2, 4, 1]
def odd_product(seq):
    is_present = False
    for i in range(len(seq)):
        for j in seq:
            if seq[i] != j:
                if seq[i] * j % 2 == 1:
                    is_present = True
    return is_present

def increasing_big(n):
    val = 0
    list = []
    increase = 0
    for i in range(n):
        list.append(val)
        increase += 2
        val += increase
    return list

print(increasing_big(10))