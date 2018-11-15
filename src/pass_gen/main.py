import argparse as arp
import random as rnd

ALPHABET_LO = "abcdefghijklmnopqrstuvwxyz"
ALPHABET_UP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOLS = "~!?@#$%^&*()"

def gen_letter_lo() -> str:
    return rnd.choice(ALPHABET_LO)

def gen_letter_up() -> str:
    return rnd.choice(ALPHABET_UP)

def gen_symbol() -> str:
    return rnd.choice(SYMBOLS)

def gen_digit() -> str:
    return rnd.choice("0123456789")

def gen_pass(length: int, *, symbols: bool = True, digits: bool = True) -> str:
    if length <= 0:
        raise ValueError("Cannot generate password "\
                         f"of non-positive length {length}")

    gens = [gen_letter_lo, gen_letter_up]
    if symbols:
        gens.append(gen_symbol)
    if digits:
        gens.append(gen_digit)
    base = len(gens)
    if base > length:
        raise ValueError("Cannot generate password with all required "\
                         f"categories with length {length}")

    igens = range(len(gens))
    additional = "".join(gens[rnd.choice(igens)]() for _ in range(length - base))
    return "".join(f() for f in gens) + additional

if __name__ == "__main__":
    print(gen_pass(8))
