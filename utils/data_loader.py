import random

def load_all_product_code():
    with open('../../data/product_code.txt', 'r', encoding='utf8') as file:
        codes = [line.strip() for line in file]
    return codes

def load_random_product_code():
    return random.choice(load_all_product_code())