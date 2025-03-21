#Szymon Oczki

import argparse
import os
import re
import math

def parse_args():
    parser = argparse.ArgumentParser(description="Program do szyfrowania i kryptoanalizy.")
    parser.add_argument("-p", action="store_true", help="Przygotowanie tekstu jawnego do szyfrowania")
    parser.add_argument("-e", action="store_true", help="Szyfrowanie")
    parser.add_argument("-d", action="store_true", help="Odszyfrowywanie")
    parser.add_argument("-k", action="store_true", help="Kryptoanaliza")
    return parser.parse_args()

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

def replace_polish_letters(text):
    polish_letters = {'ą':'a','Ą':'A', 'ć':'c', 'Ć':'C', 'ę':'e', 'Ę':'E', 'ł':'l', 'Ł':'L', 'ó':'o', 'Ó':'O', 'ś':'s', 'Ś':'S', 'ż':'z', 'Ż':'Z', 'ź':'z', 'Ź':'Z', 'ń':'n', 'Ń':'N'}
    filtered_text = ''
    for letter in text:
        filtered_text = ''.join((filtered_text, polish_letters.get(letter, letter)))

    return filtered_text

def prepare_text(text):
    no_polish_letters = replace_polish_letters(text)
    vigenere_ready_text = re.sub(r"[^A-Za-z]", '', no_polish_letters).lower()
    return vigenere_ready_text

def vigenere(text, key, code=True):
    key = key.lower()
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    ciphered_text = ''

    #this makes key_repeated always a tiny bit longer or equal to text that needs encryption
    key_repeated = key * (len(text) // len(key) + 1)


    for i in range(len(text)):
        letter_coded = text[i]
        shift = alphabet.index(key_repeated[i])

        #we take index of the letter to be coded aka the number of its position in the alphabet, we shift it according to the key and grab the letter from the alphabet with index fo the result
        if code == True:
            new_letter = alphabet[(alphabet.index(letter_coded) + shift)%26]
        elif code == False:
            new_letter = alphabet[(alphabet.index(letter_coded) - shift)%26]

        ciphered_text += new_letter

    return ciphered_text

def vigenere_cryptoanalysis(text, amountofvalues = 7):
    """
    Performs cyryptoanalysis on vigeneres cypher

    Args:
        text (str): text to do analysis on
        amountofvalues (int): takes that amount of values from coincidences_list into consideration when looking for key length. smaller value works better with shorter text and longer key, larger work better with longer text and shorter key. with limited testing optimal values seem to be around 5-10.
    
    """

    #counts coincidences
    coincidences_list = []

    for shift in range(1, len(text)):
        coincidences = 0

        for j in range(len(text) - shift):
            if text[j] == text[j + shift]:
                coincidences += 1

        coincidences_list.append(coincidences)


    #gets top values
    top_values = sorted(coincidences_list, reverse=True)[:amountofvalues]

    #checks indexes of top values in our coincidences list
    indexes = []

    for i in range(len(coincidences_list)):
        if coincidences_list[i] in top_values:
            indexes.append(i+1)


    #calculates gcd (greatest common denominator) across the indexes in indexes list to calculate key length
    speculated_key_length = math.gcd(indexes[0], indexes[1])
    for i in range(2,len(indexes)-1):
        speculated_key_length = math.gcd(speculated_key_length, indexes[i])

    print(f"Spekulowana długość klucza: {speculated_key_length}")


    #add a list to V_groups contaning every letter in a group
    V_groups = []
    for i in range(speculated_key_length):
        group = []
        index = i
        while index < len(text):
            group.append(text[index])
            index += speculated_key_length
        V_groups.append(group)

    #swaps the letters for their frequencies in promilles
    for i in range(len(V_groups)):
        group_percentages = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 
                             'j': 0, 'k': 0, 'l': 0, 'm': 0, 'n': 0, 'o': 0, 'p': 0, 'q': 0, 'r': 0, 
                             's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0}

        #counter
        for letter in V_groups[i]:
            group_percentages[letter] += 1

        V_groups[i] = group_percentages

        #swaps into promilles
        total_group_letter = 0
        for value in V_groups[i].values():
            total_group_letter += value

        for letter, value in V_groups[i].items():
            V_groups[i][letter] = (value / total_group_letter) * 1000

    W_vector_list = [82, 15, 28, 43, 127, 22, 20, 61, 70, 2, 8, 40, 24, 67, 75, 29, 1, 60, 63, 91, 28, 10, 23, 1, 20, 1]
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    key_found = ''
    for V_vector in V_groups:

        V_vector_list = list(V_vector.values())

        heighest_score = (0, 0)

        for i in range(26):
            W_vector_shifted = W_vector_list[-i:] + W_vector_list[:-i] 

            scalar_product = sum(v * w for v, w in zip(V_vector_list, W_vector_shifted))

            if heighest_score[0] < scalar_product:
                heighest_score = (scalar_product, i)

        key_found += alphabet[heighest_score[1]]

    return key_found
            
            

        


def main():
    args = parse_args()

    if sum([args.p, args.e, args.d, args.k]) != 1:
        raise ValueError("Należy wybrać dokładnie jedną operację: -p, -e, -d lub -k.")
    
    if args.p:
        print("Przygotowanie tekstu jawnego do szyfrowania...")

        text = read_file("orig.txt")
        vigenere_ready_text = prepare_text(text)

        write_in_file("plain.txt", vigenere_ready_text)

    elif args.e:
        print("Wykonywanie szyfrowania...")

        key = read_file('key.txt')
        text_to_cipher = read_file('plain.txt')
        ciphered_text = vigenere(text_to_cipher, key, code=True)

        write_in_file('crypto.txt', ciphered_text)

    elif args.d:
        print("Wykonywanie odszyfrowywania...")

        key = read_file('key.txt')
        text_to_decipher = read_file('crypto.txt')
        deciphered_text = vigenere(text_to_decipher, key, code=False)

        write_in_file('decrypt.txt', deciphered_text)

    elif args.k:
        print("Wykonywanie kryptoanalizy...")

        text_to_decipher = read_file('crypto.txt')

        key_found = vigenere_cryptoanalysis(text_to_decipher, amountofvalues=7)

        deciphered_text = vigenere(text_to_decipher, key_found, code=False)
        write_in_file('key-found.txt', key_found)
        write_in_file('decrypt.txt', deciphered_text)

if __name__ == "__main__":
   main()
