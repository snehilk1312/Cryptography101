#!/usr/bin/env python3

'''

this code has been taken from the following link:

"https://github.com/pakesson/diy-ecb-penguin/blob/master/encrypt_image.py"

and updated slightly

128 bit aes encryption is used in this code

'''


from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
from cryptography.hazmat.backends import default_backend
import os
from argparse import ArgumentParser
from cryptography.hazmat.primitives import padding

def encrypt_image(image, key, iv=b''):
	image_array = bytes(image.tobytes())
	padder = padding.PKCS7(128).padder()
	padded_data = padder.update(image_array)
	padded_data += padder.finalize()
	image_array = padded_data


	mode = modes.CBC(iv) if iv else modes.ECB()
	cipher = Cipher(algorithms.AES(key), mode, backend=default_backend())
	encryptor = cipher.encryptor()
	cipher_text = encryptor.update(image_array) + encryptor.finalize()
	padding_length = 16 - len(image_array) % 16
	cipher_text = cipher_text[:-padding_length]	# not must

	#decryptor = cipher.decryptor()
	#decrypted_text = decryptor.update(cipher_text) + decryptor.finalize()

	return Image.frombytes("RGB", image.size, cipher_text, "raw", "RGB")



if __name__ == "__main__":
	parser = ArgumentParser(description="Encrypt images with AES ECB/CBC")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("-cbc", "--cbc", action="store_true")
	group.add_argument("-ecb", "--ecb", action="store_true")

	parser.add_argument("input_file", help="Input file")
	parser.add_argument("output_file", help="Output file")
	args = parser.parse_args()


	image = Image.open(args.input_file).convert('RGBA').convert('RGB')
	key = os.urandom(16)

	if args.ecb:
		encrypt_image(image, key).save(args.output_file)
	else:
		iv = os.urandom(16)
		encrypt_image(image, key, iv).save(args.output_file)
