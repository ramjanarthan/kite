from constants import *
from primitives import Trigram, Bigram

def generate_base_vocab():
    base = allowed_characters
    base.union({space_character, tab_character, new_line_character})
    for number in numeric_characters:
        if number in base:
            base.remove(number)
    base.add(number_mask_character)

    return base

def generate_trigram_vocab():
    all_chars = generate_base_vocab()
    vocabulary = []

    for first in all_chars:
        for second in all_chars:
            for third in all_chars:
                trigram = Trigram(first, second, third)
                vocabulary += [trigram]
    
    return vocabulary

def generate_bigram_vocab():
    all_chars = generate_base_vocab()
    vocabulary = []

    for first in all_chars:
        for second in all_chars:
            trigram = Bigram(first, second)
            vocabulary += [trigram]
    
    return vocabulary