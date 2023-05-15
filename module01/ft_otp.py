import hashlib
import hmac
import os
import struct
import time
import argparse
import base64


def Banner():
        print("""                                                                      
    ______            __      
   / __/ /_    ____  / /_____ 
  / /_/ __/   / __ \/ __/ __ )
 / __/ /_    / /_/ / /_/ /_/ /
/_/  \__/____\____/\__/ .___/ 
       /_____/       /_/      


coded by KHASEY               
        """)
KEY_FILE = "ft_otp.key"
DIGITS = 6
STEP = 30

def main():
    Banner()
    parser = argparse.ArgumentParser(description="Generate one-time passwords using HOTP algorithm")
    parser.add_argument("-g",type=str, help="generate and encrypt a new key")
    parser.add_argument("-k",type=str, help="generate a new one-time password using the key")
    args = parser.parse_args()

    if args.g:
        with open(args.g, "r") as f:
            key2 = f.read().strip()
            if len(key2) < 64:
                print("error: key must be 64 hexadecimal characters.")
                exit(1)
        key = generate_key()

    
        write_key(key)
        print("Key generated and stored in {}".format(KEY_FILE))
        return

    if args.k:
        with open(KEY_FILE, "r") as f:
            key = f.read().strip()
        counter = int(time.time() / STEP)
        password = generate_otp(key, counter)
        print("{:06d}".format(password))
        return

    parser.print_help()

def generate_key():
    key = base64.b32encode(bytearray.fromhex(''.join([f'{i:02x}' for i in os.urandom(32)]))).decode()
    return key

def write_key(key):
    with open(KEY_FILE, "w") as f:
        f.write(key)


def get_key():
    with open(KEY_FILE, "r") as f:
            key = f.read().strip()
            print(key)
            if len(key) < 64:
                print(key)
                print("error: key must be 64 hexadecimal characters.")
                exit(1)

def generate_otp(key, counter):
    key_bytes = base64.b32decode(key, True)
    msg = struct.pack(">Q", counter)
    h = hmac.new(key_bytes, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

if __name__ == "__main__":
    main()
