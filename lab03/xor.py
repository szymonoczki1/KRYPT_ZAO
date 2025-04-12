#Szymon Oczki

import argparse
import os
import re

def parse_args():
    parser = argparse.ArgumentParser(description="Program do szyfrowania i kryptoanalizy.")
    parser.add_argument("-p", action="store_true", help="Przygotowanie tekstu jawnego do szyfrowania")
    parser.add_argument("-e", action="store_true", help="Szyfrowanie")
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

def read_file_to_array(file_name: str) -> list:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [re.sub(r"[^A-Za-z ]", '', line) for line in file]
    return lines


def prepare_text(text):
    text = re.sub(r"[^A-Za-z ]", '', text).lower()
    return text

def newline64(text):
    return '\n'.join(text[i:i+64] for i in range(0, len(text), 64))

def xor_chars(c1: str, c2: str):
    return hex(ord(c1) ^ ord(c2))


def code_xor(key: str, text_array: list):
    coded_arr = []
    for line in text_array:
        coded_line = ""
        #counter = 0
        for i in range(len(line)):
            key_character = key[i]
            text_character = line[i]

            #print(f"coding key_char: {key_character} and text_char {text_character}")

            xor_char = xor_chars(key_character, text_character)
            #counter += 1
            #print(f"coded char : {xor_char}, counter: {counter}")

            coded_line += xor_char

        coded_arr.append(coded_line)


    return "\n".join(coded_arr)

def decrypt_xor(key, encoded_2d_array):
    decrypted_message = []

    temp_string = ""

    for row in encoded_2d_array:
        for idx, hex_value in enumerate(row):

            if key[idx] == "_":
                decrypted_char = "_"
            else:
                int_value = int(hex_value, 16)
                decrypted_char = chr(int_value ^ ord(key[idx]))

            temp_string += decrypted_char

        decrypted_message.append(temp_string)
        temp_string = ""

    return decrypted_message


def split_coded_msg_64_2darray(hex_string, chunk_size=64):
    hex_numbers = hex_string.split("0x")[1::]
    
    for i in range(len(hex_numbers)):
        hex_numbers[i] = hex_numbers[i].strip()

    return [hex_numbers[i:i + chunk_size] for i in range(0, len(hex_numbers), chunk_size)]

def cryptoanalysis_xor(text_arr):
    key = ["_"] * len(text_arr[0])


    #left to right
    for i in range(len(text_arr[0])):
        foundkey = 0

        #picks first element
        for j in range(len(text_arr)-1):
            if foundkey == 1:
                break
            hex1 = int(text_arr[j][i], 16)

            #compares the rest to first element
            for k in range(j+1, len(text_arr)-2):
                hex2 = int(text_arr[k][i], 16)
                hex3 = int(text_arr[k+1][i], 16)

                xor_val1 = hex1 ^ hex2
                xor_val2 = hex2 ^ hex3
                xor_val3 = hex1 ^ hex3

                if f"{xor_val1:08b}"[:3] == "010" and f"{xor_val2:08b}"[:3] != "010":
                    space_hex = hex1
                elif f"{xor_val1:08b}"[:3] != "010" and f"{xor_val2:08b}"[:3] == "010":
                    space_hex = hex3
                elif f"{xor_val1:08b}"[:3] == "010" and f"{xor_val2:08b}"[:3] == "010" and xor_val3 != 0:
                    space_hex = hex2
                else:
                    continue

                recovered_char = chr(space_hex ^ 0x20)

                if recovered_char.isprintable() and len(recovered_char) == 1 and re.match(r'^[a-zA-Z ]$', recovered_char):
                    foundkey = 1
                    key[i] = recovered_char
                    #print(f"Recovered key for position {i}: {key[i]}")
                    break

    return key



    





def main():
    args = parse_args()

    if sum([args.p, args.e, args.k]) != 1:
        raise ValueError("Należy wybrać dokładnie jedną operację: -p, -e lub -k.")
    
    if args.p:
        print("Przygotowanie tekstu jawnego do szyfrowania...")

        text = read_file("orig.txt")

        text = prepare_text(text)
        text = newline64(text)

        write_in_file("plain.txt", text)

    elif args.e:
        print("Wykonywanie szyfrowania...")

        text = read_file_to_array("plain.txt")
        key = read_file_to_array("key.txt")
        key = key[0]


        coded_xor = code_xor(key, text)

        write_in_file("crypto.txt", coded_xor)


    elif args.k:
        print("Wykonywanie kryptoanalizy...")

        coded_msg = read_file("crypto.txt")
        parsed_coded_msg = split_coded_msg_64_2darray(coded_msg)


        key = cryptoanalysis_xor(parsed_coded_msg)

        decrypted_msg = decrypt_xor(key, parsed_coded_msg)

        write_in_file("decrypt.txt", "\n".join(decrypted_msg))


        pass

if __name__ == "__main__":
   main()