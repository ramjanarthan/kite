from tokenizers import BigramTokenizer, TrigramTokenizer
from collections import defaultdict
import pickle

def calculate_trigram_counts(filename):
    count_map = defaultdict(lambda: 0)
    tokenizer = TrigramTokenizer(filename)

    while next_trigram := tokenizer.next():
        count_map[next_trigram] += 1
    
    return count_map

def calculate_bigram_counts(filename):
    count_map = defaultdict(lambda: 0)
    tokenizer = BigramTokenizer(filename)

    while next_bigram := tokenizer.next():
        count_map[next_bigram] += 1
    
    return count_map

# trigram_counts_en = calculate_trigram_counts('data/python/split/train_processed')
# bigram_counts_en = calculate_bigram_counts('data/python/split/train_processed')

# # Testing
# c = 0
# for (key, value) in trigram_counts_en.items():
#     print(f"key: {key} value: {value}")
#     c += 1s
#     if c > 20: 
#         break

# c = 0
# for (key, value) in bigram_counts_en.items():
#     print(f"key: {key} value: {value}")
#     c += 1
#     if c > 20: 
#         break