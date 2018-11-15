import argparse
from random import choice
import sys

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

def make_parser() -> 'argparse.ArgumentParser':
    p = argparse.ArgumentParser(\
            description="Simple password utility."\
            " Generated passwords may include latin characters of both case,"\
            f" special characters (\"{SYMBOLS}\") and digits")
    p.add_argument('-l', '--length',
        help = "Specify the length of desired password",
        metavar = "length",
        dest = 'length',
        type = int,
        action = 'store',
        default = 8)
    p.add_argument('--skip-symbols',
        help = "Do not use special characters for generating password",
        action = 'store_true',
        dest = 'skip_symbols')
    p.add_argument('--skip-digits',
        help = "Do not use digits for generating password",
        action = 'store_true',
        dest = 'skip_digits')
    return p

if __name__ == "__main__":
    parser = make_parser()
    args = parser.parse_args()
    
    try:
        password = gen_pass(args.length,
                 symbols = not args.skip_symbols,
                 digits = not args.skip_digits)
    except ValueError as err:
        print(err, file = sys.stderr)
        sys.exit()
    
    print(password)
