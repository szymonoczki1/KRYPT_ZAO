#Szymon Oczki


import os
import argparse
import re

def read_file(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    lines = []
    with open(file_path, "r", encoding='utf-8') as file:
        for line in file:
            lines.append(line)

    return lines

def write_in_file(file_name, text):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    with open(file_path, "w", encoding='utf-8') as file:
        file.write(text)

def read_mess_hex_to_bit(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    with open(file_path, "r") as file:
        hex_string = file.read().strip()

    binary_string = bin(int(hex_string, 16))[2:]
    return binary_string.zfill(len(hex_string) * 4)

def parse_args():
    parser = argparse.ArgumentParser(description="Program do steganografii.")
    parser.add_argument("-e", action="store_true", help="encode")
    parser.add_argument("-d", action="store_true", help="decode")
    parser.add_argument("-1", dest="opt1", action="store_true", help="option 1")
    parser.add_argument("-2", dest="opt2", action="store_true", help="option 2")
    parser.add_argument("-3", dest="opt3", action="store_true", help="option 3")
    parser.add_argument("-4", dest="opt4", action="store_true", help="option 4")
    return parser.parse_args()

def bit_string_to_hex(bit_string):
    if len(bit_string) % 4 != 0:
        bit_string = bit_string.ljust((len(bit_string) + 3) // 4 * 4, '0')

    hex_string = hex(int(bit_string, 2))[2:]
    return hex_string.upper()

def option_1_e(line_array, bit_string):
    if len(bit_string) > len(line_array):
        raise ValueError("Not enough lines in the file to encode all bits of the message.")

    for i in range(len(line_array)):
        if line_array[i].endswith('\n'):
            line_array[i] = line_array[i].rstrip(' \t\n') + '\n'
        else:
            line_array[i] = line_array[i].rstrip(' \t')

    for index, char in enumerate(bit_string):
        if char == '1':
            if not line_array[index].endswith(' \n'):
                if line_array[index].endswith('\n'):
                    line_array[index] = line_array[index][:-1] + ' \n'
                else:
                    line_array[index] = line_array[index] + ' '
            

    return ''.join(line_array)

def option_1_d(line_array):
    bit_string = ''

    for line in line_array:
        if line.endswith(' \n'):
            bit_string += '1'
        elif line.endswith('\n'):
            bit_string += '0'

    
    #bit_string = bit_string.rstrip('0')
    #print(f"Bit string: {bit_string}")

    hex_string = bit_string_to_hex(bit_string)
    return hex_string

def option_2_e(line_array, bit_string):

    text = ''.join(line_array)
    text = re.sub(r' +', ' ', text)

    space_indices = [i for i, c in enumerate(text) if c == ' ']
    
    if len(bit_string) > len(space_indices):
        raise ValueError("Not enough spaces in the file to encode all bits of the message.")

    added_spaces = 0
    text = list(text)

    for index, char in enumerate(bit_string):
        space_index = space_indices[index] + added_spaces
        if char == '1':
            text.insert(space_index, ' ')
            added_spaces += 1

    return ''.join(text)
    

def option_2_d(line_array):
    text = ''.join(line_array)
    bit_string = ''

    i = 0
    while i < len(text):
        if text[i] == ' ':
            if i + 1 < len(text) and text[i + 1] == ' ':
                bit_string += '1'
                i += 2
            else:
                bit_string += '0'
                i += 1
        else:
            i += 1

    #print(f"Bit string: {bit_string}")

    

    hex_string = bit_string_to_hex(bit_string)
    return hex_string

def option_3_e(line_array, bit_string):
    text = ''.join(line_array)
    p_tags = list(re.finditer(r'<p( [^>]*)?>', text, re.IGNORECASE))
    if len(bit_string) > len(p_tags):
        raise ValueError("Not enough <p> tags to encode all bits of the message.")

    new_text = text
    offset = 0
    for idx, bit in enumerate(bit_string):
        match = p_tags[idx]
        insert_pos = match.end() + offset - 1
        if bit == '0':
            insert_str = ' style="margin-botom: 0cm;"'
        else:
            insert_str = ' style="lineheight: 100%;"'
        new_text = new_text[:insert_pos] + insert_str + new_text[insert_pos:]
        offset += len(insert_str)
    return new_text

def option_3_d(line_array):
    text = ''.join(line_array)
    p_tags = list(re.finditer(r'<p[^>]*>', text, re.IGNORECASE))
    bit_string = ''
    for tag in p_tags:
        tag_text = tag.group()
        if 'margin-botom' in tag_text:
            bit_string += '0'
        elif 'lineheight' in tag_text:
            bit_string += '1'
    #print(f"Bit string: {bit_string}")
    hex_string = bit_string_to_hex(bit_string)
    return hex_string

def option_4_e(line_array, bit_string):
    text = ''.join(line_array)
    # Find all <FONT ...></FONT> pairs
    font_pairs = list(re.finditer(r'(<FONT[^>]*></FONT>)', text, re.IGNORECASE))

    if len(bit_string) > len(font_pairs):
        raise ValueError("Not enough <FONT> tags to encode all bits of the message.")

    new_text = text
    offset = 0

    for idx, bit in enumerate(bit_string):
        match = font_pairs[idx]
        start, end = match.start() + offset, match.end() + offset
        original = match.group()
        if bit == '1':
            insert_str = '<FONT></FONT>' + original
            new_text = new_text[:start] + insert_str + new_text[end:]
            offset += len('<FONT></FONT>')
        else:
            insert_str = original + '<FONT></FONT>'
            new_text = new_text[:start] + insert_str + new_text[end:]
            offset += len('<FONT></FONT>')
    return new_text

def option_4_d(line_array):
    text = ''.join(line_array)
    bit_string = ''
    pattern = re.compile(r'(<FONT[^>]+></FONT>|<FONT></FONT>)', re.IGNORECASE)
    tags = list(pattern.finditer(text))
    i = 0
    while i < len(tags) - 1:
        tag1 = tags[i].group()
        tag2 = tags[i + 1].group()
        if re.match(r'<FONT></FONT>', tag1, re.IGNORECASE) and re.match(r'<FONT[^>]+></FONT>', tag2, re.IGNORECASE):
            bit_string += '1'
            i += 2
        elif re.match(r'<FONT[^>]+></FONT>', tag1, re.IGNORECASE) and re.match(r'<FONT></FONT>', tag2, re.IGNORECASE):
            bit_string += '0'
            i += 2
        else:
            i += 1
    #print(f"Bit string: {bit_string}")
    hex_string = bit_string_to_hex(bit_string)
    return hex_string

def main():
    args = parse_args()

    if args.e:
        if args.opt1:
            print("Encoding option 1 selected.")
            lines = read_file("cover.html")
            bit_string = read_mess_hex_to_bit("mess.txt")

            output = option_1_e(lines, bit_string)
            write_in_file("watermark.html", output)
        elif args.opt2:
            print("Encoding option 2 selected.")
            lines = read_file("cover.html")
            bit_string = read_mess_hex_to_bit("mess.txt")

            output = option_2_e(lines, bit_string)
            write_in_file("watermark.html", output)
        elif args.opt3:
            print("Encoding option 3 selected.")
            lines = read_file("cover.html")
            bit_string = read_mess_hex_to_bit("mess.txt")

            output = option_3_e(lines, bit_string)
            write_in_file("watermark.html", output)
        elif args.opt4:
            print("Encoding option 4 selected.")
            lines = read_file("cover.html")
            bit_string = read_mess_hex_to_bit("mess.txt")

            output = option_4_e(lines, bit_string)
            write_in_file("watermark.html", output)
    elif args.d:
        if args.opt1:
            print("Decoding option 1 selected.")
            output_lines = read_file("watermark.html")
            hex_string = option_1_d(output_lines)
            write_in_file("detect.txt", hex_string)
        elif args.opt2:
            print("Decoding option 2 selected.")
            output_lines = read_file("watermark.html")
            hex_string = option_2_d(output_lines)
            write_in_file("detect.txt", hex_string)
        elif args.opt3:
            print("Decoding option 3 selected.")
            output_lines = read_file("watermark.html")
            hex_string = option_3_d(output_lines)
            write_in_file("detect.txt", hex_string)
        elif args.opt4:
            print("Decoding option 4 selected.")
            output_lines = read_file("watermark.html")
            hex_string = option_4_d(output_lines)
            write_in_file("detect.txt", hex_string)




    

    

if __name__ == "__main__":
    main()