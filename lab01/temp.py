def find_inverse_a(a):
    for i in range(1, 26):
        if (a*i)%26 == 1:
            return i
    return None

i = 9

print(i, find_inverse_a(i))