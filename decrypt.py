from pydoc import plain
from PIL import Image
import string
import utils


def decryption(img):
    # This function will extract the hidden encoded message from the image and decode it
    image = Image.open(img, 'r')
    plainText = ''
    imageData = iter(image.getdata())
    while True:
        pixels = [value for value in imageData.__next__(
        )[:3] + imageData.__next__()[:3] + imageData.__next__()[:3]]
        binaryFormatString = ''
        # odd RGB value means 0, even RGB value means 1
        for i in pixels[:8]:
            if i % 2 != 0:
                binaryFormatString += '0'
            else:
                binaryFormatString += '1'
        plainText += chr(int(binaryFormatString, 2))
        # when the 9th pixel is odd, decode end
        if pixels[-1] % 2 != 0:
            print("The hiden message is: " + plainText)
            return plainText


def text_decrypt_caesar_cipher(ciphertext, key):
    '''
    name: text_decrypt_caesar_cipher
    parameter: ciphertext(a string that is encoded by Caesar cipher) and a key(an integer)
    return: plaintext (a string that is decrypted by Caesar cipher from the ciphertect)
    '''

    # to ensure key is an integer(positive or negative)
    if not isinstance(key, int):
        raise TypeError('Key should be an integer')

    # to validate ciphertext
    if not isinstance(ciphertext, str):
        raise TypeError('ciphertext should be a string')
    if len(ciphertext) == 0:
        raise ValueError('ciphertext should have at least 1 letter')

    # strip the punctuation out
    for c in ciphertext:
        if c in string.punctuation:
            ciphertext = ciphertext.replace(c, '')
    # strip the space out
    ciphertext = ciphertext.replace(' ', '')

    if not ciphertext.isalpha():
        raise ValueError('all characters in ciphertext should be alphabet')

    # to adjust format of the ciphertext
    ciphertext = ciphertext.upper()

    # to calculate the position difference between ciphertext and plaintext
    original = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    move_position = key % len(original)

    # to build the encoded alphabet
    encoded = ''
    encoded = encoded + original[move_position:] + original[:move_position]

    # to match from ciphertext to plaintext
    plaintext = ''
    for letters in ciphertext:
        plaintext += original[encoded.index(letters)]

    return plaintext


def text_decrypt_railfence_cipher(ciphertext, key):
    '''
    name: encrypt()
    parameter: ciphertext transformed from plaintext by rail fence encrytion, letters only; key-an integer value
    return: plaintext decrypted from ciphertext by rail fence encrytion
    '''

    # validate ciphertext
    if not isinstance(ciphertext, str):
        raise TypeError('ciphertext should be a string')
    if len(ciphertext) == 0:
        raise ValueError('ciphertext should have at least 1 letter')
    ciphertext = utils.strip(ciphertext)
    if not ciphertext.isalpha():
        raise ValueError('all characters in ciphertext should be alphabet')

    ciphertext = ciphertext.upper()

    # validate key
    if not isinstance(key, int):
        raise TypeError('Key should be an integer')
    if key < 2:
        raise ValueError('key should be at least 2')
    if key > len(ciphertext):
        print('You might want to use a different key... this one is too big')

    group = (key - 2) * 2 + 2
    n = len(ciphertext) // group
    # to calculate how many letters in each rail
    rails = {}
    for i in range(1, key + 1):
        if i == 1 or i == key:
            rails[i] = n
        else:
            rails[i] = 2 * n
    rest = len(ciphertext) % group
    if rest > 0 and rest <= key:
        i = 1
        while i <= rest:
            rails[i] += 1
            i += 1
    elif rest > key:
        i = 1
        while i <= rest:
            if i <= key:
                rails[i] += 1
            else:
                x = key - (i - key)
                rails[x] += 1
            i += 1

    # to build dictionay rails of texts
    ct = ciphertext
    rail_text = {}
    for i in range(1, key + 1):
        rail_text[i] = ct[:rails[i]]
        ct = ct.replace(ct[:rails[i]], '', 1)

    plaintext = ''
    # rotate n number of groups
    for num in range(n):
        # matching plaintext within each group
        i = 1
        while i <= group:
            if i <= key and len(rail_text[i]) > 0:
                plaintext += rail_text[i][0]
                rail_text[i] = rail_text[i].replace(rail_text[i][0], '', 1)
            elif i > key:
                x = 2 * key - i
                if len(rail_text[x]) > 0:
                    plaintext += rail_text[x][0]
                    rail_text[x] = rail_text[x].replace(rail_text[x][0], '', 1)
            i += 1

    # matching plaintext outside of a complete group
    i = 1
    while i <= rest:
        if i <= key and len(rail_text[i]) > 0:
            plaintext += rail_text[i][0]
            rail_text[i] = rail_text[i].replace(rail_text[i][0], '', 1)
        elif i > key:
            x = 2 * key - i
            if len(rail_text[x]) > 0:
                plaintext += rail_text[x][0]
                rail_text[x] = rail_text[x].replace(rail_text[x][0], '', 1)
        i += 1

    return plaintext


def text_decrypt_combined(ciphertext, key):
    half_decryped = text_decrypt_railfence_cipher(ciphertext, key)
    full_decrypted = text_decrypt_caesar_cipher(half_decryped, key)
    return full_decrypted


def main():
    img = "encrypted_image.png"
    decryption(img)

    key = 4
    ciphertext_caesar = "LIPPSASVPH"
    ciphertext_rf = "HOEWRLOLLD"
    ciphertext_combined = "LSIAVPSPPH"

    caesar_decrypted = text_decrypt_caesar_cipher(ciphertext_caesar, key)
    print("Decryped text from caesar cipher is: " + caesar_decrypted)
    rf_decrypted = text_decrypt_railfence_cipher(ciphertext_rf, key)
    print("Decryped text from railfence cipher is: " + rf_decrypted)
    combined_decrypted = text_decrypt_combined(ciphertext_combined, key)
    print("Decryped text from combined algorithms is: " + combined_decrypted)


if __name__ == "__main__":
    main()
