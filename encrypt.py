from PIL import Image
import os
from pydoc import plain
import string
import utils


# encode img
def processImage(pixels, data):
    # This function will convert the encoded message from ascii binary form into pixels
    # For example, H = 01001000, we will use 3 pixels(3*3 RBG value) to
    # store the 8 bits. We define odd RBG value corresponds to 0, even RBG value to 1.
    # Let's say the original R value of the first pixel is 18, then we need to increase it
    # to 19 because 19 is an odd value which corresponds to 0.
    # We also need to set each 9th pixel value to even value. By doing that, as long as we
    # set the 9th pixel value of last character to odd, we know this is the end of the msg.
    binaryFormMsg = []
    for i in data:
        # generate the corresponding ascii code for the data
        binary_data = format(ord(i), '08b')
        binaryFormMsg.append(binary_data)
    lengthOfMsg = len(binaryFormMsg)
    imageData = iter(pixels)
    for idx in range(lengthOfMsg):
        pixels = [val for val in imageData.__next__(
        )[:3] + imageData.__next__()[:3] + imageData.__next__()[:3]]
        for bit in range(8):
            if (binaryFormMsg[idx][bit] == '1') and (pixels[bit] % 2 != 0):
                pixels[bit] -= 1
            elif (binaryFormMsg[idx][bit] == '0') and (pixels[bit] % 2 == 0):
                if pixels[bit] == 0:
                    pixels[bit] += 1
                pixels[bit] -= 1
        bit = 8
        if pixels[bit] % 2 != 0:
            pixels[bit] += 1
            pixels[bit] %= 255
        if idx == (lengthOfMsg-1):
            if pixels[-1] % 2 == 0:
                if pixels[-1] == 0:
                    pixels[-1] += 1
                else:
                    pixels[-1] -= 1
        pixels = tuple(pixels)
        yield pixels[:3]
        yield pixels[3:6]
        yield pixels[6:9]


def updateImagePixel(img, data):
    # This method will encode data to the new image that will be created
    size = img.size[0]
    (col, row) = (0, 0)
    for pixel in processImage(img.getdata(), data):
        img.putpixel((col, row), pixel)
        if size-1 == col:
            col = 0
            row += 1
        else:
            col += 1


def encryption(img, text):
    # This function will encode the msg and hide it into the image.
    # Then generate an encrypted image called "encrypted_image.png".
    image = Image.open(img, 'r')
    if (len(text) == 0):
        print("No message inputed!")
        return
    if (len(img) == 0):
        print("No image inputed!")
        return
    # output the encoded img
    newImage = image.copy()
    updateImagePixel(newImage, text)
    newImageName = 'encrypted_image.png'
    newImage.save(newImageName, 'png')
    # print("encrypted image path:" + os.path.abspath("encrypted_image.png"))
    return os.path.abspath("encrypted_image.png")


def text_encrypt_caesar_cipher(plaintext, key):
    '''
    name: text_encrypt_caesar_cipher
    parameter: a string that is the plaintext that needs to be encoded, an integer as a key
    return: a ciphertext string that returned from encoding plaintext by caesar cipher method.
    '''

    # to ensure key is valid (integer)
    if not isinstance(key, int):
        raise TypeError('Key should be an integer')
    if key % 26 == 0:
        print('This key is not helping, please use another key.')

    # to ensure the plaintext is valid(string)
    if not isinstance(plaintext, str):
        raise TypeError('plaintext should be a string')
    elif len(plaintext) == 0:
        raise ValueError('plaintext should have at least 1 letter')

    plaintext = utils.strip(plaintext)

    if not plaintext.isalpha():
        raise ValueError('all characters in plaintext should be alphabet')

    # to adjust format of plaintext
    plaintext = plaintext.upper()

    # to calculate the position different from plaintext to ciphertext
    original = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    move_position = key % len(original)

    # to build the encoded alphabet
    encoded = ''
    encoded = encoded + original[move_position:] + original[:move_position]

    # to match from plaintext to ciphertext
    ciphertext = ''
    for letter in plaintext:
        ciphertext += encoded[original.index(letter)]

    return ciphertext


def text_encrypt_railfence_cipher(plaintext, key):
    '''
    name: encrypt()
    parameter: plaintext-string texts that needs to be encoded, letters only; key-an integer value
    return: ciphertext transformed from plaintext by rail fence encrytion
    '''
    # validate plaintext
    if not isinstance(plaintext, str):
        raise TypeError('plaintext should be a string')
    elif len(plaintext) == 0:
        raise ValueError('plaintext should have at least 1 letter')
    plaintext = utils.strip(plaintext)
    if not plaintext.isalpha():
        raise ValueError('all characters in plaintext should be alphabet')
    plaintext = plaintext.upper()

    # validate key
    if not isinstance(key, int):
        raise TypeError('Key should be an integer')
    if key < 2:
        raise ValueError('key should be at least 2')
    if key > len(plaintext):
        print('Key should be no longer than the length of the plaintext that you want to encrypt')

    # calculate number of rails
    end = 2
    middle = key - 2
    group = end + middle * 2

    # build a dict including a group of rails (end rails + middle rails*2)
    group_dict = {}
    for i in range(1, group + 1):
        group_dict[i] = []

    # place letters in rails (middle rails are seperated to two parts)
    r = 1
    for letter in plaintext:
        group_dict[r].append(letter)
        if r < group:
            r += 1
        elif r == group:
            r = 1

    # combine the two seperated middle rails into one
    if key > 2:
        mid_dict = {}
        for i in range(1, middle + 1):
            mid_dict[i] = ''
            for letter in group_dict[i + 1]:
                mid_dict[i] += letter + ' '
            x = 0
            while x < len(group_dict[group + 1 - i]):
                y = group_dict[group + 1 - i][x]
                mid_dict[i] = mid_dict[i].replace(' ', y, 1)
                x += 1
            mid_dict[i] = utils.strip(mid_dict[i])

    # print out ciphertext
    start_rail = ''
    for letter in group_dict[1]:
        start_rail += letter
    end_rail = ''
    for letter in group_dict[key]:
        end_rail += letter
    mid_rails = ''
    for i in range(1, middle + 1):
        mid_rails += mid_dict[i]
    ciphertext = start_rail + mid_rails + end_rail

    return ciphertext


def text_encrypt_combined(plaintext, key):
    half_encrypted = text_encrypt_caesar_cipher(plaintext, key)
    full_encrypted = text_encrypt_railfence_cipher(half_encrypted, key)
    return full_encrypted


def main():
    text = "Hello World!!!"
    img = "vancouver1.jpg"
    key = 4

    caesar_encrypted = text_encrypt_caesar_cipher(text, key)
    print("Cipher text after caesar cipher encryption is: " + caesar_encrypted)
    rf_encrypted = text_encrypt_railfence_cipher(text, key)
    print("Cipher text after rail fence cipher encryption is: " + rf_encrypted)
    combined_encrypted = text_encrypt_combined(text, key)
    print("Encryped text from combined algorithems is: " + combined_encrypted)
    encryption(img, text)


if __name__ == "__main__":
    main()
