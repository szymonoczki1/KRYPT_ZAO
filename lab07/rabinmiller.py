#Szymon Oczki

import random
import os
import argparse

def read_file(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    lines = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            lines.append(int(line))

    return lines

def write_in_file(file_name, text):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    with open(file_path, "w", encoding='utf-8') as file:
        file.write(text)

def parse_args():
    parser = argparse.ArgumentParser(description="Program z algorytmem Rabina-Millera lub Fermata.")
    parser.add_argument("-f", action="store_true", help="Algorytm Fermata")
    return parser.parse_args()

def parse_input_file(file_name):
    lines = read_file(file_name)

    n = lines[0]
    r = None
    if len(lines) >= 2:
        r = lines[1]
        if len(lines) >= 3:
            r = (r * lines[2]) - 1

    return n, r

def gcd(a, b):
    while b:
        temp = b
        b = a % b
        a = temp
    return a

def mod_exp(a, e, n):
    result = 1
    a = a % n
    while e > 0:
        if e % 2 == 1:
            result = (result * a) % n
        a = (a * a) % n
        e //= 2
    return result

def fermat_test(n, rounds=40):
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        #print(a, gcd(a, n))
        if gcd(a, n) != 1:
            #continue
            return "divisorexists", gcd(a, n)
        if mod_exp(a, n - 1, n) != 1:
            return "compositenum", None
    return "maybeprime", None

def rabin_miller_test(n, rounds=40, r=None):
    if r is None:
        r = n - 1
    m = r
    k = 0
    while m % 2 == 0:
        m //= 2
        k += 1

    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        d = gcd(a, n)
        if d != 1:
            return "divisorexists", d

        b = mod_exp(a, m, n)
        if b == 1 or b == n - 1:
            continue
        for _ in range(k - 1):
            b = (b * b) % n
            if b == n - 1:
                break
            if b == 1:
                return "compositenum", None
        else:
            return "compositenum", None
    return "maybeprime", None

def main():
    args = parse_args()

    n, r = parse_input_file('wejscie.txt')

    if args.f:
        result, data = fermat_test(n)
    else:
        result, data = rabin_miller_test(n, r=r)
        
    if result == "divisorexists":
        write_in_file('wyjscie.txt', str(data))
    elif result == "compositenum":
        write_in_file('wyjscie.txt', "na pewno złożona")
    elif result == "maybeprime":
        write_in_file('wyjscie.txt', "prawdopodobnie pierwsza")

if __name__ == "__main__":
    main()
