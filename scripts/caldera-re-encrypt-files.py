#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: David Espejo (Fortytwo Security)

from cryptography.fernet import Fernet
import os

def load_key(key_string):
    # load the key from the provided string
    return key_string.encode()

def decrypt_file(file_path, key):
    # use the key to decrypt the contents of the file
    with open(file_path, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(data)

    return decrypted_data

def encrypt_file(file_path, data, key):
    # use the key to encrypt the data and write it to the file
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)

    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

def main():
    old_key = load_key('OLD_KEY') # Replace with your old key
    new_key = load_key('NEW_KEY') # Replace with your new key
    file_path = 'data/object_store' # Replace with the path to your file

    decrypted_data = decrypt_file(file_path, old_key)
    encrypt_file(file_path, decrypted_data, new_key)

if __name__ == '__main__':
    main()
