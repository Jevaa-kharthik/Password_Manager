# Command Line Password Manager

This command-line password manager application securely stores and manages user passwords. The program allows the user to store new passwords, retrieve existing passwords, and generate strong random passwords.

## Features

- Store new passwords securely by encrypting them using a master password provided by the user.
- Retrieve passwords by decrypting them using the master password.
- Generate strong random passwords based on user-specified length and complexity requirements.

## Requirements

- `Python 3.x` Newer 3.11
- `cryptography` library

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/password_manager.git
    cd password_manager
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
3. **To Run the Program**:
   ```sh
   python3 password_manager.py
   ```

## Usage

### Store a Password

```sh
python password_manager.py --operation store --master-password mysecretpassword --service gmail --password mygmailpassword
```
### To Retrive a Password

```sh
python password_manager.py --operation retrieve --master-password mysecretpassword --service gmail
```
### Generate a Strong Password

```sh
python password_manager.py --operation generate --length 12 --complexity 2

