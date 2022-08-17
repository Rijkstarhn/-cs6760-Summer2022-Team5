import utils
import encrypt
import decrypt


def main():
    try:
        task = str(input('Menu: \nEncrypt (E)\nDecrypt (D)\n'))
        task = utils.strip(task).upper()
        if task == 'E':
            text_encryption_algorithm = str(input(
                'Which algorithm would you like to use to encrypt your message?\nCaesar (C)\nRailFence (R)\nBoth (B)\n'))
            text_encryption_algorithm = utils.strip(
                text_encryption_algorithm).upper()
            if text_encryption_algorithm != "C" and text_encryption_algorithm != "R" and text_encryption_algorithm != "B":
                exit("Invalid option. Bye!")
            # get user input for message, key and img option
            plaintext = str(input('What is your message:\n'))
            key = int(input('What is the key? (Integer between 2-9)\n'))
            img = str(input(
                'Choose an img from the following options:\nImage1.jpg (1)\nImage2.jpg (2)\nImage3.jpg (3)\nImage4.jpg (4)\n'))
            if img == "1":
                img = "vancouver1.jpg"
            elif img == "2":
                img = "vancouver4.jpg"
            elif img == "3":
                img = "Silicon_Valley_Campus.jpg"
            else:
                img = "SFBA.jpg"

            # step 1: text encryption - Caesar Cipher algorithm
            if text_encryption_algorithm == "C":
                encrypted = encrypt.text_encrypt_caesar_cipher(
                    plaintext, key)
                print("Cipher text after caesar cipher encryption is: " + encrypted)

            # step 1: text encryption - Rail Fence Cipher algorithm
            elif text_encryption_algorithm == "R":
                encrypted = encrypt.text_encrypt_railfence_cipher(
                    plaintext, key)
                print(
                    "Cipher text after rail fence cipher encryption is: " + encrypted)

            # step 1: text encryption - Combined algorithm
            elif text_encryption_algorithm == "B":
                encrypted = encrypt.text_encrypt_combined(
                    plaintext, key)
                print("Encryped text from combined algorithems is: " + encrypted)

            # step 2: img encryption
            lsb_encrypted = encrypt.encryption(img, encrypted)

            print("Your message is encrypted here: " + lsb_encrypted)

        elif task == 'D':
            # get user input for message, key and img location
            text_encryption_algorithm = str(input(
                'Which algorithm did you use to encrypt your message?\nCaesar(C)\nRailFence(R)\nBoth(B)\n'))
            text_encryption_algorithm = utils.strip(
                text_encryption_algorithm).upper()
            if text_encryption_algorithm != "C" and text_encryption_algorithm != "R" and text_encryption_algorithm != "B":
                exit("Invalid option. Bye!")
            key = int(input('What is the key? (Integer between 2-9)\n'))
            img = str(
                input('What is the filepath to your encrypted img?\n'))

            # step 1: img decrytion
            lsb_decrypted = decrypt.decryption(img)

            # step 2: text decryption - Caesar Cipher algorithm
            if text_encryption_algorithm == "C":
                caesar_decrypted = decrypt.text_decrypt_caesar_cipher(
                    lsb_decrypted, key)
                print("Original message is: " + caesar_decrypted)

            # step 2: text decryption - Rail Fence Cipher algorithm
            elif text_encryption_algorithm == "R":
                rf_decrypted = decrypt.text_decrypt_railfence_cipher(
                    lsb_decrypted, key)
                print("Original message is: " + rf_decrypted)

            # step 2: text decryption - Combined algorithm
            elif text_encryption_algorithm == "B":
                combined_decrypted = decrypt.text_decrypt_combined(
                    lsb_decrypted, key)
                print("Original message is: " + combined_decrypted)

        else:
            exit("Invalid option. Bye!")
    except Exception as ex:
        print('Error found', str(ex))


if __name__ == "__main__":
    main()
