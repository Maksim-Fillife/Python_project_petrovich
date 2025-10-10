from pathlib import Path
import random

DATA_DIR = Path(__file__).parent.parent / "data"

def load_all_product_code():
    codes = DATA_DIR / "product_codes.txt"
    with open(codes, encoding='utf8') as file:
        codes = [line.strip() for line in file]
    return codes

def load_random_product_code():
    return random.choice(load_all_product_code())