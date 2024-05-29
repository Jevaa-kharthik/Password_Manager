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
        with open(STORAGE_FILE, 'w') as file:
            file.write('{}')
        return {}
    try:
        with open(STORAGE_FILE, 'r') as file:
            content = file.read()
            if not content.strip():
                return {}
            return json.loads(content)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        print("Error: Invalid JSON data in {}. Resetting storage.".format(STORAGE_FILE))
        with open(STORAGE_FILE, 'w') as reset_file:
            reset_file.write('{}')
        return {}

def save_storage(storage):
    with open(STORAGE_FILE, 'w') as file:
        json.dump(storage, file, indent=4)

def store_password(master_password, service, password):
    storage = load_storage()
    key = generate_key(master_password)
    encrypted_password = encrypt(password, key)
    storage[service] = encrypted_password
    save_storage(storage)
    print("Password for {} stored successfully.".format(service))

def retrieve_password(master_password, service):
    storage = load_storage()
    if service not in storage:
        print(f"No password found in {service}.")
        return
    key = generate_key(master_password)
    try:
        decrypted_password = decrypt(storage[service], key)
        print("Password for {} : {}".format(service, decrypted_password))
    except InvalidToken:
        print("Invalid Main password.")

def generate_password(length, complexity):
    characters = string.ascii_letters + string.digits
    if complexity >= 2:
        characters += string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    print("Generated password: {}".format(password))
    return password

def main():
    parser = argparse.ArgumentParser(description='Command Line Password Manager')
    parser.add_argument('--operation', required=True, choices=['store', 'retrieve', 'generate'], help='There are three Operation to Perform (1. Store 2.Retrieve 3. Generate)')
    parser.add_argument('--master-password', help='Master password for encryption/decryption of the main password')
    parser.add_argument('--service', help='Service name for the password Ex.Gmail, Facebook')
    parser.add_argument('--password', help='Original Password of the Service')
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
