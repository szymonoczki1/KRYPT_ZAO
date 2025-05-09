#Szymon Oczki

from PIL import Image
import hashlib
import numpy as np
import os

BLOCK_SIZE = 8  # 8x8 pixeli
IV = b'\x00' * 64  # inicjalny wektor dla CBC pelny zer w tym przypadku, kazda hex liczba dziala
#IV = os.urandom(64) wektor z losowymi bajtami

def read_key(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    key = b''
    try:
        with open(file_path, 'rb') as file:
            key = file.read()
    except FileNotFoundError:
        pass

    return key

def load_image(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    img = Image.open(file_path).convert('1')  # 1 = czarno-biały
    return np.array(img, dtype=np.uint8)

def save_image(data, file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)

    img = Image.fromarray(data * 255).convert('1')
    img.save(file_path)

def get_blocks(img_array):
    h, w = img_array.shape
    blocks = []
    for y in range(0, h, BLOCK_SIZE):
        for x in range(0, w, BLOCK_SIZE):
            block = img_array[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE] # dzieli na bloki
            if block.shape == (BLOCK_SIZE, BLOCK_SIZE):
                blocks.append((y, x, block.copy())) # dodaj blok i x y koordynaty
    return blocks

def hash_block(block, key=b''):
    data = block.flatten().tobytes() + key # sha512 potrzebuje byte inputu zeby nie bylo typeerror
    digest = hashlib.sha512(data).digest()
    return np.array(list(digest[:BLOCK_SIZE*BLOCK_SIZE]), dtype=np.uint8).reshape((BLOCK_SIZE, BLOCK_SIZE)) % 2 #bierzemy 64 bajty -> lista zamienia bajty na int -> zamieniamy na np array zeby zrobic reshape 8x8 2d -> % 2 zeby zamienic na 0-1

def ecb_encrypt(blocks, img_shape, key=b''):
    encrypted = np.zeros(img_shape, dtype=np.uint8) #czarny obraz
    for y, x, block in blocks:
        encrypted[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE] = hash_block(block, key) #zastepujemy miejsca blokow zahashowanymi blokami z oryginalnego obrazu
    return encrypted

def xor_blocks(block1, block2):
    return np.bitwise_xor(block1, block2)

def cbc_encrypt(blocks, img_shape, key=b''):
    encrypted = np.zeros(img_shape, dtype=np.uint8) #czarny obraz
    prev_cipher = np.frombuffer(IV, dtype=np.uint8).reshape((BLOCK_SIZE, BLOCK_SIZE)) % 2 #frombuffer zamienia bajty na int -> z naszego pierwszego wektora do xora robimy pseudo blok
    for y, x, block in blocks:
        xored = xor_blocks(block, prev_cipher)
        cipher = hash_block(xored, key)
        encrypted[y:y+BLOCK_SIZE, x:x+BLOCK_SIZE] = cipher
        prev_cipher = cipher
    return encrypted

def main():
    key = read_key('key.txt')
    

    img = load_image('plain.bmp')
    blocks = get_blocks(img)

    ecb_result = ecb_encrypt(blocks, img.shape, key)
    save_image(ecb_result, 'ecb_crypto.bmp')

    cbc_result = cbc_encrypt(blocks, img.shape, key)
    save_image(cbc_result, 'cbc_crypto.bmp')

if __name__ == '__main__':
    main()
