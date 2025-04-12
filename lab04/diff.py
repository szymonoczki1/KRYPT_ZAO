#Szymon Oczki


import os


def read_file_to_array(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    lines = []
    with open(file_path, "r", encoding='utf-8') as file:
        for line in file:
            lines.append(line.strip())

    return lines

def write_in_file(file_name, text):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    with open(file_path, "w", encoding='utf-8') as file:
        file.write(text)



def compare_bits_verbose(hex1, hex2):
    bytes1 = bytes.fromhex(hex1.strip())
    bytes2 = bytes.fromhex(hex2.strip())

    if len(bytes1) != len(bytes2):
        raise ValueError("Hex1 and Hex2 must be of equal length.")

    total_bits = len(bytes1) * 8
    diff_bits = 0

    # bit_str1 = ""
    # bit_str2 = ""
    # diff_line = ""

    for b1, b2 in zip(bytes1, bytes2):
        b1_bits = format(b1, '08b')
        b2_bits = format(b2, '08b')
        # bit_str1 += b1_bits
        # bit_str2 += b2_bits

        for bit1, bit2 in zip(b1_bits, b2_bits):
            if bit1 != bit2:
                diff_bits += 1
            #     diff_line += "^"
            # else:
            #     diff_line += " "

    percent_diff = (diff_bits / total_bits) * 100

    #print("HEXTOBIT1: ", bit_str1)
    #print("HEXTOBIT2: ", bit_str2)
    #print("DIFFSTR", diff_line)
    #print(f"Liczba różnych bitów: {diff_bits} z {total_bits}")
    #print(f"Procent różnych bitów: {percent_diff:.2f}%")

    return f"Liczba różniących sie bitów: {diff_bits} z {total_bits}, procentowo: {percent_diff:.2f}%\n"


def process_hash(arr):
    for i in range(0, len(arr), 5):
        if i + 2 < len(arr) and i + 3 < len(arr):
            hex1 = arr[i + 2]
            hex2 = arr[i + 3]
            result = compare_bits_verbose(hex1, hex2)
            if i + 4 < len(arr):
                arr[i + 4] = result
            else:
                arr.append(result)
    return arr


def main():
    lines = read_file_to_array("hash.txt")
    arr = process_hash(lines)
    text = "\n".join(arr)
    write_in_file("diff.txt", text)

if __name__ == "__main__":
   main()

