import argparse as arp
from random import choice

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET_LO = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOLS = "~!?@#$%^&*()"
DIGITS = "0123456789"

def gen_pass(length: int, *, symbols: bool = True, digits: bool = True) -> str:
    if length <= 0:
        raise ValueError("Cannot generate password "\
                         f"of non-positive length {length}")

    required = [choice(ALPHABET_LO), choice(ALPHABET_UP)]
    charset = ALPHABET
    if symbols:
        required.append(choice(SYMBOLS))
        charset += SYMBOLS
    if digits:
        required.append(choice(DIGITS))
        charset += DIGITS

    base = len(required)
    if base > length:
        raise ValueError("Cannot generate password with all required "\
                         f"categories with length {length}")

    additional = "".join(choice(charset) for _ in range(length - base))
    return "".join(required) + additional

if __name__ == "__main__":
    print(gen_pass(8))
