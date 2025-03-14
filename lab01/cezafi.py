import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description="Program do szyfrowania i kryptoanalizy.")
    parser.add_argument("-c", action="store_true", help="Szyfr Cezara")
    parser.add_argument("-a", action="store_true", help="Szyfr afiniczny")
    parser.add_argument("-e", action="store_true", help="Szyfrowanie")
    parser.add_argument("-d", action="store_true", help="Odszyfrowywanie")
    parser.add_argument("-j", action="store_true", help="Kryptoanaliza z tekstem jawnym")
    parser.add_argument("-k", action="store_true", help="Kryptoanaliza bez tekstu jawnego")
    return parser.parse_args()

def check_files(required_files):
    missing_files = [f for f in required_files if not os.path.exists(f)]
    if missing_files:
        print(f"Brak wymaganych plików: {', '.join(missing_files)}")
        exit(1)

def replace_polish_letters(text):
    polish_letters = {'ą':'a','Ą':'A', 'ć':'c', 'Ć':'C', 'ę':'e', 'Ę':'E', 'ł':'l', 'Ł':'L', 'ó':'o', 'Ó':'O', 'ś':'s', 'Ś':'S', 'ż':'z', 'Ż':'Z', 'ź':'z', 'Ź':'Z', 'ń':'n', 'Ń':'N'}
    filtered_text = ''
    for letter in text:
        filtered_text = ''.join((filtered_text, polish_letters.get(letter, letter)))

    return filtered_text

def read_file(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    text = ''
    with open(file_path, "r", encoding='utf-8') as file:
        text = file.read().strip()

    return text

def write_in_file(file_name, text):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    with open(file_path, "w", encoding='utf-8') as file:
        file.write(text)

def plaintext_cryptanalysis(caesar = True):
    coded_text = read_file('crypto.txt')
    plain_text = read_file('extra.txt')

    if caesar:
        found = False

        for i in range(min(len(coded_text), len(plain_text))):
            if coded_text[i].isalpha():
                first_letter_coded = ord(coded_text[i])
                first_letter_plain = ord(plain_text[i])
                found = True
                break

        if not found:
            raise ValueError("Znalezienie klucza jest niemożliwe. (Brak znaków alfabetycznych do porównania)") 

        key = first_letter_coded - first_letter_plain

        write_in_file('key-found.txt', str(key))
    else:
        pair1 = [None,None]
        pair2 = [None,None]
        lower_case_start = 97
        upper_case_start = 65
        pair_found = False

        for i in range(min(len(coded_text), len(plain_text))):
            if coded_text[i].isalpha():
                if coded_text[i].isupper():
                    offset = upper_case_start
                else:
                    offset = lower_case_start

                c_letter = ord(coded_text[i]) - offset
                p_letter = ord(plain_text[i]) - offset

                for j in range(i + 1, min(len(coded_text), len(plain_text))):
                    if coded_text[j].isalpha():
                        if coded_text[j].isupper():
                            offset = upper_case_start
                        else:
                            offset = lower_case_start

                        c_letter_j = ord(coded_text[j]) - offset
                        p_letter_j = ord(plain_text[j]) - offset

                        delta_p = (p_letter - p_letter_j) % 26
                        if find_inverse_a(delta_p) != None:
                            pair1 = [p_letter, c_letter]
                            pair2 = [p_letter_j, c_letter_j]
                            pair_found = True
                            break
                if pair_found:
                    break

        if pair1[0] is None or pair2[0] is None:
            raise ValueError("Znalezienie klucza jest niemożliwe. (Brak możliwości rozwiązania równania z podanych liter / Brak wystarczającej ilości znaków alfabetycznych)") 

        p1_letter, c1_letter = pair1
        p2_letter, c2_letter = pair2

        delta_p = (p1_letter - p2_letter) % 26
        delta_c = (c1_letter - c2_letter) % 26

        inverse_delta_p = find_inverse_a(delta_p)

        a = (delta_c * inverse_delta_p) % 26

        b = (c1_letter - a * p1_letter) % 26
        
        key = f"{a} {b}"

        write_in_file('key-found.txt', key)

def no_plaintext_cryptoanalysis(caesar = True):
    coded_text = read_file('crypto.txt')
    possible_answers = []
    if caesar:
        for i in range(1, 26):
            possible_answers.append(code_caesar(i, coded_text, code=False))

        text = "\n".join(possible_answers)
        write_in_file('decrypt.txt', text)
    else:
        valid_a_values = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
        for a in valid_a_values:
            for b in range(26):
                decoded_text = code_affine((a,b), coded_text, code=False)
                if decoded_text != coded_text:
                    possible_answers.append(decoded_text)
        text = "\n".join(possible_answers)
        write_in_file('decrypt.txt', text)

def code_caesar(key, text, code=True):
    '''code arg has to be set to false to decode the cypher'''
    lower_case_start = 97
    upper_case_start = 65

    coded_text = ''

    for letter in text:
        if letter.isalpha():
            if letter.islower():
                offset = lower_case_start
            elif letter.isupper():
                offset = upper_case_start
            
            if code == True:
                coded_ascii_val = ((ord(letter) - offset + key) % 26) + offset
            else:
                coded_ascii_val = ((ord(letter) - offset - key) % 26) + offset

            coded_letter = chr(coded_ascii_val)
        else:
            coded_letter = letter
            
        coded_text += coded_letter

    return coded_text

def code_affine(key, text, code=True):
    lower_case_start = 97
    upper_case_start = 65

    coded_text = ''

    for letter in text:
        if letter.isalpha():
            if letter.islower():
                offset = lower_case_start
            elif letter.isupper():
                offset = upper_case_start
            
            if code == True:
                coded_ascii_val = (((key[0] * (ord(letter) - offset)) + key[1]) % 26) + offset
            else:
                inverse_a = find_inverse_a(key[0])
                coded_ascii_val = ((inverse_a * ((ord(letter) - offset) - key[1])) % 26) + offset

            coded_letter = chr(coded_ascii_val)
        else:
            coded_letter = letter
            
        coded_text += coded_letter

    return coded_text

def is_key_valid(key, caesar=True):
    if caesar == True:
        if key >= 1 and key <= 25:
            return True
        else:
            raise ValueError("Klucz jest nie poprawny. (Kluczem powinna być liczba w zakresie 0-26)") 
    elif caesar == False:
        if key[0] not in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:
            raise ValueError("Klucz jest niepoprawny (NWD miedzy a, a 26 powinno byc rowne 1)")
        else:
            return True

def find_inverse_a(a):
    for i in range(1, 26):
        if (a*i)%26 == 1:
            return i
    return None

def main():
    args = parse_args()
    
    if args.c and args.a:
        raise ValueError("Nie można używać jednocześnie szyfru Cezara i afinicznego.")
    
    if sum([args.e, args.d, args.j, args.k]) != 1:
        raise ValueError("Należy wybrać dokładnie jedną operację: -e, -d, -j lub -k.")
    
    required_files = []
    if args.e:
        required_files = ["plain.txt", "key.txt"]
        write_in_file("plain.txt", replace_polish_letters(read_file("plain.txt")))
    elif args.d:
        required_files = ["crypto.txt", "key.txt"]
    elif args.j:
        required_files = ["crypto.txt", "extra.txt"]
        write_in_file("extra.txt", replace_polish_letters(read_file("extra.txt")))
    elif args.k:
        required_files = ["crypto.txt"]
    
    check_files(required_files)


    
    if args.c:
        if args.e:
            print("Wykonywanie szyfrowania...")

            key = int(read_file('key.txt').split()[0])
            
            if not is_key_valid(key, caesar=True):
                raise ValueError("incorrect key value")
            
            coded_text_caesar = code_caesar(key, read_file('plain.txt'), code=True)
            write_in_file('crypto.txt', coded_text_caesar)
        elif args.d:
            print("Wykonywanie odszyfrowywania...")

            key = int(read_file('key.txt').split()[0])

            if not is_key_valid(key, caesar=True):
                raise ValueError("incorrect key value")
            
            decoded_text_caesar = code_caesar(key, read_file('crypto.txt'), code=False)
            write_in_file('decrypt.txt', decoded_text_caesar)
        elif args.j:
            print("Wykonywanie kryptoanalizy z tekstem jawnym...")

            plaintext_cryptanalysis(caesar=True)
            key = int(read_file('key-found.txt').split()[0])
            decoded_text_caesar = code_caesar(key, read_file('crypto.txt'), code=False)
            write_in_file('decrypt.txt', decoded_text_caesar)
        elif args.k:
            print("Wykonywanie kryptoanalizy bez tekstu jawnego...")

            no_plaintext_cryptoanalysis(caesar=True)
    elif args.a:
        if args.e:
            print("Wykonywanie szyfrowania...")

            key = read_file('key.txt').split()
            key = (int(key[0]), int(key[1]))

            if not is_key_valid(key, caesar=False):
                raise ValueError("incorrect key value")
            
            coded_text_affine = code_affine(key, read_file('plain.txt'), code=True)
            write_in_file('crypto.txt', coded_text_affine)
        elif args.d:
            print("Wykonywanie odszyfrowywania...")

            key = read_file('key.txt').split()
            key = (int(key[0]), int(key[1]))
            
            if not is_key_valid(key, caesar=False):
                raise ValueError("incorrect key value")
            
            coded_text_affine = code_affine(key, read_file('crypto.txt'), code=False)
            write_in_file('decrypt.txt', coded_text_affine)
        elif args.j:
            print("Wykonywanie kryptoanalizy z tekstem jawnym...")

            plaintext_cryptanalysis(caesar=False)
            key = read_file('key-found.txt').split()
            key = (int(key[0]), int(key[1]))
            decoded_text_affine = code_affine(key, read_file('crypto.txt'), code=False)
            write_in_file('decrypt.txt', decoded_text_affine)
        elif args.k:
            print("Wykonywanie kryptoanalizy bez tekstu jawnego...")

            no_plaintext_cryptoanalysis(caesar=False)

if __name__ == "__main__":
    main()