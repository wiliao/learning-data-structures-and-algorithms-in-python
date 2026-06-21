from random import *

def checkmatches(n):
    birthdays = []

    for i in range(n):
        val = randint(0, 1460)
        val = val // 4
        birthdays.append(val)

    matches = False

    for i in range(n):
        for j in range(n):
            try:
                if birthdays[i] == birthdays[i + j + 1]:
                    matches = True
            except:
                pass

    #print(birthdays)
    return matches

checkmatches(23)

def checkBatchMatches(n, trials):
    matches = 0
    for i in range(trials):
        if checkmatches(n):
            matches += 1
    return matches / trials

print(checkBatchMatches(57, 10000))