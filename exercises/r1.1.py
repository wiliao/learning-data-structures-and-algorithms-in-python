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

import random
list = [1, 2, 3, 4, 5, 67]

def shuffle(list):
    new_list = []
    for i in range(len(list)):
        new_list.append("placeholder")
    for i in range(len(list)):
        spot = random.randint(0, len(list) - 1)
        while new_list[spot] != "placeholder":
            spot = random.randint(0, len(list) - 1)
        new_list[spot] = list[i]
    return new_list

def reverser():
    plist = []
    try:
        while True:
            item = input("Enter an item: ")
            plist.append(item)
    except EOFError:
        for i in range(len(plist)):
            print(plist[-1 * i - 1])

def oub():
    spot = int(input("Enter a number: "))
    list = [0, 0, 0]
    try:
        list[spot] = 1
    except IndexError:
        print("Out of bounds")

def norm(v, p = 2):
    thing = sum([abs(n) ** p for n in v]) ** (1 / p)
    thing = round(thing * 100000) / 100000
    return thing

def permutator():
    list = ['c', 'a', 't', 'd', 'o', 'g']
    perms = []
    for i in range(999999):
        perm = str(i)
        if '1' in perm and '2' in perm and '3' in perm and '4' in perm and '5' in perm and '6' in perm:
            perms.append(perm)
    for j in perms:
        print(list[int(j[0]) - 1] + list[int(j[1]) - 1] + list[int(j[2]) - 1] + list[int(j[3]) - 1] + list[int(j[4]) - 1] + list[int(j[5]) - 1])

def stringToList(string):
    return [char for char in string]

def make_change(value):
    coins = [100, 50, 20, 10, 5, 2, 1, 0.25, 0.1, 0.05]
    needed = []
    
    for i in coins:
        need = 0
        while value >= i:
            need += 1
            value = value - i
        needed.append(need)
    return needed


