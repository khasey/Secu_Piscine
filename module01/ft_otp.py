from cryptography.fernet import Fernet
import datetime
import hmac
import hashlib
import base64
import argparse
import sys
import os


FILE_KEY_PATH = 'key.hex'
ENCRYPTED_KEY_PATH = 'ft_otp.key'
GREEN = '\033[92m'
RESET = '\033[0m'
RED = '\033[91m'

def Banner():
        print(GREEN + """                                                                      
    ______            __      
   / __/ /_    ____  / /_____ 
  / /_/ __/   / __ \/ __/ __ )
 / __/ /_    / /_/ / /_/ /_/ /
/_/  \__/____\____/\__/ .___/ 
       /_____/       /_/      
coded by KHASEY               
        """)


def decrypt_key():
    with open(FILE_KEY_PATH, 'rb') as filekey:
        key = filekey.read()
    
    with open(ENCRYPTED_KEY_PATH, 'rb') as encrypted_keyfile:
        encrypted_key = encrypted_keyfile.read()

    cipher = Fernet(key)
    decrypted_key = cipher.decrypt(encrypted_key)
    return decrypted_key.decode()


def key_generator():
    hex_key = decrypt_key()
    hashed = hmac.new(base64.b16decode(hex_key, casefold=True), int(time_counter()).to_bytes(8, byteorder='big'), hashlib.sha1)
    digest = hashed.hexdigest()
    offset = int(digest[-1], 16)
    bin_code = bin(int(digest[offset*2:offset*2+8], 16))
    
    otp = int(bin_code[3:], 2) % 10**6 if len(bin_code[2:]) > 31 else int(bin_code[2:], 2) % 10**6
    
    print(str(otp).zfill(6))


def time_counter():
    dt = datetime.datetime.now(datetime.timezone.utc)
    dt_min = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
    dt = dt - (dt - dt_min) % datetime.timedelta(seconds=30)
    utc_time = dt.replace(tzinfo=datetime.timezone.utc)
    utc_timestamp = utc_time.timestamp()
    return int(utc_timestamp) // 30


def generate_key_file():
    if not os.path.isfile(FILE_KEY_PATH):
        os.system(f"touch {FILE_KEY_PATH} 2> /dev/null")
        print(GREEN + 'File ' + RED + f'{FILE_KEY_PATH} ' + GREEN + 'created' + RESET)

        key = Fernet.generate_key()
        with open(FILE_KEY_PATH, 'wb') as filekey:
            filekey.write(key)
            print(GREEN + 'Key generated' + RESET)


def encrypt_key(key):
    if len(key) == 64:
        mykey = key
        print('Indicateur -g activé')

        if not os.path.isfile(FILE_KEY_PATH):
            os.system(f"touch {ENCRYPTED_KEY_PATH} 2> /dev/null")
            print(GREEN + f'{ENCRYPTED_KEY_PATH} ' + GREEN + 'created' + RESET)

        if os.path.isfile('key.key'):
            user_input = input('You are about to generate a new key, this process will permanently erase the old key. Do you wish to continue? [y][N]')

            if user_input.lower() != 'y':
                os.system('clear')
                sys.exit(1)

            print(GREEN + 'Processing to create a new key ' + RESET)

        with open(FILE_KEY_PATH, 'rb') as filekey:
            key = filekey.read()

        cipher = Fernet(key)
        encrypted_key = cipher.encrypt(mykey.encode())

        with open(ENCRYPTED_KEY_PATH, 'wb') as keyfile:
            keyfile.write(encrypted_key)
            print(GREEN + 'Encrypted key written to ft_otp.key.' + RESET)
    else:
        print(RED+"The key must contain 64 characters"+RESET)
        sys.exit(1)


def main():
    Banner()
    parser = argparse.ArgumentParser(description='Encrypted key generator')
    parser.add_argument('-g', type=str, help="generate and encrypt a new key")
    parser.add_argument('-k', action='store_true', help="generate a new one-time password using the key")
    args = parser.parse_args()

    # generate_key_file()

    if not any(vars(args).values()):#si il ny a pas d argument il print une usage
        parser.print_usage()
        sys.exit(1)

    if args.g and not args.k:
        generate_key_file()
        if args.g == 'key.hex' and os.path.isfile('./key.hex'):
            mykey = open('key.hex', 'r').read()
            with open(FILE_KEY_PATH, 'rb') as filekey:
                key = filekey.read()
            cipher = Fernet(key)
            encrypted_key = cipher.encrypt(mykey.encode())
            with open(ENCRYPTED_KEY_PATH, 'wb') as keyfile:
                keyfile.write(encrypted_key)
                print(GREEN + 'Encrypted key written to ft_otp.key.' + RESET)

        elif len(args.g) == 64:
            encrypt_key(args.g)
        else:
            print("The key must contain 64 characters")
            sys.exit(1)

    if args.k and not args.g:
        if not os.path.isfile(ENCRYPTED_KEY_PATH):
            print('Key not found, generate a key with ft_otp -g <hexadecimal key of at least 64 characters>')
        else:
            key_generator()

main()
