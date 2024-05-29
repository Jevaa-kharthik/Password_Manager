import argparse
import json
import os
from encryption import encrypt, decrypt, generate_key
from cryptography.fernet import InvalidToken
import secrets
import string

STORAGE_FILE = 'storage.json'

def load_storage():
    if not os.path.exists(STORAGE_FILE):
        return {}
    with open(STORAGE_FILE, 'r') as file:
        return json.load(file)

def save_storage(storage):
    with open(STORAGE_FILE, 'w') as file:
        json.dump(storage, file, indent=4)

def store_password(master_password, service, password):
    storage = load_storage()
    key = generate_key(master_password)
    encrypted_password = encrypt(password, key)
    storage[service] = encrypted_password
    save_storage(storage)
    print(f"Password for {service} stored successfully.")

def retrieve_password(master_password, service):
    storage = load_storage()
    if service not in storage:
        print(f"No password found for {service}.")
        return
    key = generate_key(master_password)
    try:
        decrypted_password = decrypt(storage[service], key)
        print(f"Password for {service}: {decrypted_password}")
    except InvalidToken:
        print("Invalid master password.")

def generate_password(length, complexity):
    characters = string.ascii_letters + string.digits
    if complexity >= 2:
        characters += string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    print(f"Generated password: {password}")
    return password

def main():
    parser = argparse.ArgumentParser(description='Command Line Password Manager')
    parser.add_argument('--operation', required=True, choices=['store', 'retrieve', 'generate'], help='Operation to perform')
    parser.add_argument('--master-password', help='Master password for encryption/decryption')
    parser.add_argument('--service', help='Service name for the password')
    parser.add_argument('--password', help='Password to store')
    parser.add_argument('--length', type=int, help='Length of the password to generate')
    parser.add_argument('--complexity', type=int, choices=[1, 2], default=1, help='Complexity of the password to generate (1: Alphanumeric, 2: Alphanumeric + Special Characters)')

    args = parser.parse_args()

    if args.operation == 'store':
        if not args.master_password or not args.service or not args.password:
            parser.error("--master-password, --service, and --password are required for storing a password")
        store_password(args.master_password, args.service, args.password)
    elif args.operation == 'retrieve':
        if not args.master_password or not args.service:
            parser.error("--master-password and --service are required for retrieving a password")
        retrieve_password(args.master_password, args.service)
    elif args.operation == 'generate':
        if not args.length:
            parser.error("--length is required for generating a password")
        generate_password(args.length, args.complexity)

if __name__ == "__main__":
    main()
