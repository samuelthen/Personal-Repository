import json
import pikepdf
from tqdm import tqdm
import itertools
import argparse

# Argument parser setup
parser = argparse.ArgumentParser(description="PDF Password Cracker")
parser.add_argument('pdf_file', type=str, help='The path to the PDF file to decrypt')
args = parser.parse_args()

# Load configuration
with open('config.json', 'r') as file:
    config = json.load(file)

prefix = config.get("prefix", "")
suffix = config.get("suffix", "")
max_length = 20
total_length = config.get("total_length", None)

characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Generate combinations and try to open the PDF with each password
password_found = False

# If total_length is not provided, try every length up to max_length
if total_length is None:
    for length in range(1, max_length - len(prefix) - len(suffix) + 1):
        guess_length = length
        combinations = [''.join(p) for p in itertools.product(characters, repeat=guess_length)]
        passwords = [prefix + combination + suffix for combination in combinations]

        for password in tqdm(passwords, f"Trying passwords of length {length + len(prefix) + len(suffix)}"):
            try:
                with pikepdf.open(args.pdf_file, password=password) as pdf:
                    print("\n[+] Password found:", password)
                    password_found = True
                    break
            except pikepdf.PasswordError:
                continue
        
        if password_found:
            break
else:
    guess_length = total_length - len(prefix) - len(suffix)
    if guess_length < 0:
        raise ValueError("The total length must be greater than the combined length of prefix and suffix.")
    combinations = [''.join(p) for p in itertools.product(characters, repeat=guess_length)]
    passwords = [prefix + combination + suffix for combination in combinations]

    for password in tqdm(passwords, "Decrypting PDF"):
        try:
            with pikepdf.open(args.pdf_file, password=password) as pdf:
                print("\n[+] Password found:", password)
                password_found = True
                break
        except pikepdf.PasswordError:
            continue

if not password_found:
    print("[-] Password not found.")
