import encrypt
import decrypt
import io
import os
import unittest.mock
import SkepticEncryption

class Test(unittest.TestCase):

    # SkepticEnctyption
    # to test if user input wrong option, the program will exit with error message
    @unittest.mock.patch('builtins.input', side_effect=['A'])
    def test_user_input_wrong_option(self, mock_inputs):
        with self.assertRaises(SystemExit) as error:
            SkepticEncryption.main()
        self.assertEqual(str(error.exception), 'Invalid option. Bye!')

    # to test the Caesar encryption method encrypt and decrypt correctly
    @unittest.mock.patch('builtins.input', side_effect=['E', 'C', 'TEST', 2, 1, 'D', 'C', 2, 'encrypted_image.png'])
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_Caesar_encryption_method(self, mock_stdout, mock_inputs):
        SkepticEncryption.main()
        SkepticEncryption.main()
        self.assertTrue('Original message is: TEST' in str(mock_stdout.getvalue()))

    # to test the railfence encryption method encrypt and decrypt correctly
    @unittest.mock.patch('builtins.input', side_effect=['E', 'R', 'TEST', 2, 1, 'D', 'R', 2, 'encrypted_image.png'])
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_Railfence_encryption_method(self, mock_stdout, mock_inputs):
        SkepticEncryption.main()
        SkepticEncryption.main()
        self.assertTrue('Original message is: TEST' in str(mock_stdout.getvalue()))

    # to test the combined encryption method encrypt and decrypt correctly
    @unittest.mock.patch('builtins.input', side_effect=['E', 'B', 'TEST', 2, 1, 'D', 'B', 2, 'encrypted_image.png'])
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_combined_encryption_method(self, mock_stdout, mock_inputs):
        SkepticEncryption.main()
        SkepticEncryption.main()
        self.assertTrue('Original message is: TEST' in str(mock_stdout.getvalue()))

    # caesar cipher encoding and decoding
    # to test if the key is an integer
    def test_caesar_cipher_key_integer(self):
        with self.assertRaises(TypeError) as error:
            encrypt.text_encrypt_caesar_cipher('test', 'not an integer')
        self.assertEqual(str(error.exception), 'Key should be an integer')

    # to test if the key % 26 == 0
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_caesar_cipher_key_is_helping(self, mock_stdout):
        encrypt.text_encrypt_caesar_cipher('test', 26)
        self.assertEqual(mock_stdout.getvalue(), 'This key is not helping, please use another key.\n')

    # to test if the plaintext is not a string
    def test_caesar_cipher_plaintext_string(self):
        with self.assertRaises(TypeError) as error:
            encrypt.text_encrypt_caesar_cipher(1, 1)
        self.assertEqual(str(error.exception), 'plaintext should be a string')

    # to test if the length of plaintext has length
    def test_caesar_cipher_plaintext_not_len_zero(self):
        with self.assertRaises(ValueError) as error:
            encrypt.text_encrypt_caesar_cipher('', 1)
        self.assertEqual(str(error.exception), 'plaintext should have at least 1 letter')

    # to test if all characters in plaintext is alphabet
    def test_caesar_cipher_plaintext_all_alphabet(self):
        with self.assertRaises(ValueError) as error:
            encrypt.text_encrypt_caesar_cipher('a.9', 1)
        self.assertEqual(str(error.exception), 'all characters in plaintext should be alphabet')

    # to test if the caesar cipher method encodes correctly
    def test_caesar_cipher_plaintext_encoded_right(self):
        encoded = encrypt.text_encrypt_caesar_cipher('abc', 1)
        self.assertEqual(encoded, 'BCD')
        encoded = encrypt.text_encrypt_caesar_cipher('AD', 1)
        self.assertEqual(encoded, 'BE')
        encoded = encrypt.text_encrypt_caesar_cipher('abc', 49)
        self.assertEqual(encoded, 'XYZ')
        encoded = encrypt.text_encrypt_caesar_cipher('ab c', 1)
        self.assertEqual(encoded, 'BCD')

    # to test if the caesar cipher encryption method decodes correctly
    def test_caesar_cipher_plaintext_decoded_right(self):
        decoded = decrypt.text_decrypt_caesar_cipher('BCD', 1)
        self.assertEqual(decoded, 'ABC')
        decoded = decrypt.text_decrypt_caesar_cipher('BE', 1)
        self.assertEqual(decoded, 'AD')
        decoded = decrypt.text_decrypt_caesar_cipher('XYZ', 49)
        self.assertEqual(decoded, 'ABC')
        decoded = decrypt.text_decrypt_caesar_cipher('BCD', 1)
        self.assertEqual(decoded, 'ABC')


    # railfence cipher encoding and decoding
    # to test if the plaintext is not a string type
    def test_railfence_cipher_plaintext_string(self):
        with self.assertRaises(TypeError) as error:
            encrypt.text_encrypt_railfence_cipher(1, 1)
        self.assertEqual(str(error.exception), 'plaintext should be a string')

    # to test if the plaintext has length
    def test_railfence_cipher_plaintext_not_len_zero(self):
        with self.assertRaises(ValueError) as error:
            encrypt.text_encrypt_railfence_cipher('', 1)
        self.assertEqual(str(error.exception), 'plaintext should have at least 1 letter')

    # to test if all characters in plaintext is alphabet
    def test_railfence_cipher_plaintext_all_alphabet(self):
        with self.assertRaises(ValueError) as error:
            encrypt.text_encrypt_railfence_cipher('a.9', 1)
        self.assertEqual(str(error.exception), 'all characters in plaintext should be alphabet')

    # to test if the key is an integer
    def test_railfence_cipher_key_integer(self):
        with self.assertRaises(TypeError) as error:
            encrypt.text_encrypt_railfence_cipher('test', 'not an integer')
        self.assertEqual(str(error.exception), 'Key should be an integer')

    # to test if the key is at least 2
    def test_railfence_cipher_key_at_least_two(self):
        with self.assertRaises(ValueError) as error:
            encrypt.text_encrypt_railfence_cipher('test', 1)
        self.assertEqual(str(error.exception), 'key should be at least 2')

    # to test if the key is shorter than the length of plaintext
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_railfence_cipher_key_shorter_plaintext(self, mock_stdout):
        encrypt.text_encrypt_railfence_cipher('test', 5)
        self.assertEqual(mock_stdout.getvalue(), 'Key should be no longer than the length of the plaintext that you want to encrypt\n')

    # to test if the railfence cipher method encodes correctly
    def test_railfence_cipher_plaintext_encoded_right(self):
        encoded = encrypt.text_encrypt_railfence_cipher('abc', 2)
        self.assertEqual(encoded, 'ACB')
        encoded = encrypt.text_encrypt_railfence_cipher('abcdef', 4)
        self.assertEqual(encoded, 'ABFCED')

    # to test if the railfence cipher encryption method decodes correctly
    def test_railfence_cipher_plaintext_decoded_right(self):
        decoded = decrypt.text_decrypt_railfence_cipher('ACB', 2)
        self.assertEqual(decoded, 'ABC')
        decoded = decrypt.text_decrypt_railfence_cipher('ABFCED', 4)
        self.assertEqual(decoded, 'ABCDEF')

    # to test if the combined encryption method encodes correctly
    def test_combined_encoded_right(self):
        encoded = encrypt.text_encrypt_combined('abc', 2)
        self.assertEqual(encoded, 'CED')
        encoded = encrypt.text_encrypt_combined('abcdef', 4)
        self.assertEqual(encoded, 'EFJGIH')

    # to test if the combined cipher encryption method decodes correctly
    def test_combined_decoded_right(self):
        decoded = decrypt.text_decrypt_combined('CED', 2)
        self.assertEqual(decoded, 'ABC')
        decoded = decrypt.text_decrypt_combined('EFJGIH', 4)
        self.assertEqual(decoded, 'ABCDEF')


    @classmethod
    def tearDownClass(self):
        if os.path.exists("encrypted_image.png"):
            os.remove("encrypted_image.png")


if __name__ == '__main__':
    unittest.main()
