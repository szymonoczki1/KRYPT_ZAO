def mod_exp(a, e, n):
    result = 1
    a = a % n
    while e > 0:
        print(f'a= {a}, e = {e}, result = {result}')
        if e % 2 == 1:
            result = (result * a) % n
        a = (a * a) % n
        e //= 2
    return result


print(mod_exp(3, 999, 50))