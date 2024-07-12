import pikepdf
from tqdm import tqdm
import itertools

passwords = []

characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
combinations = [''.join(p) for p in itertools.product(characters, repeat=4)]

for combination in combinations:
    passwords.append("" + combination)


for password in tqdm(passwords, "Decrypting PDF"):
    try:
        with pikepdf.open("sample.pdf", password=password) as pdf:
            print("\n[+] Password found:", password)
            break
    except pikepdf.PasswordError as e:
        continue