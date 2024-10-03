from constants import SAMPLE_MODEL_FILENAME
from primitives import Bigram, Trigram, BigramDistribution
from collections import defaultdict
from generator import sample
from string import ascii_lowercase
import random

class SampleLanguageModel:
    """For a given vocabulary and set of bigrams, contains all the trigram distributions over that set of bigrams"""
    DEBUG_MODE = False

    def __init__(self, distribution_map) -> None:
        self.distribution_map = distribution_map

    def generate_next(self, context): 
        """Given a bigram 'context', generate a possible 'trigram' that is most likely that this bigram prefixes"""

        bigram_dist = self.distribution_map[context]

        if not bigram_dist:
            # For example, if context == Bigram('.', "#")
            return None
        
        sampled_trigram = sample(bigram_dist.dist)
        return sampled_trigram
    
    def generate_start(self) -> Bigram:
        """Method to sample from all possible start bigrams"""

        possibilites = [Bigram("#", ' '), Bigram("#", '.'), Bigram("#", '0'), Bigram("#", '#'), Bigram('#', 'a'), Bigram('#', 'b'), Bigram('#', 'c'), Bigram('#', 'd'), Bigram('#', 'e'), Bigram('#', 'f'), Bigram('#', 'g'), Bigram('#', 'h'), Bigram('#', 'i'), Bigram('#', 'j'), Bigram('#', 'k'), Bigram('#', 'l'), Bigram('#', 'm'), Bigram('#', 'n'), Bigram('#', 'o'), Bigram('#', 'p'), Bigram('#', 'q'), Bigram('#', 'r'), Bigram('#', 's'), Bigram('#', 't'), Bigram('#', 'u'), Bigram('#', 'v'), Bigram('#', 'w'), Bigram('#', 'x'), Bigram('#', 'y'), Bigram('#', 'z')]

        return random.choice(possibilites)


    def validate(self):
        """For a given bigram_distribution, we expect the sum of all trigram probabilites to sum to one"""
        for (key, distribution) in sorted(self.distribution_map.items()):
            sum = 0
            for (trigram, probability) in sorted(distribution.dist.items()):
                sum += probability
                if SampleLanguageModel.DEBUG_MODE:
                    print(f"sum { sum} proabbility: {probability} trigram: {trigram}")
            
            if abs(1 - sum) > 0.001:
                if SampleLanguageModel.DEBUG_MODE:
                    print(f"Error with sum: {sum} for key: {key}")
                raise Exception(f"Validation failed for model. Erronous bigram distribution: {key}")
            else:
                if SampleLanguageModel.DEBUG_MODE:
                    print(f"Valid for: {key}")
            
        return True

def parse_line(line):
    """Every line follow the pattern - *$#<tab>0000\n - three characters in the start, followed by <tab>, followed by float number, and a new line"""
    word = line[:3]
    probability = line[4:]

    bigram = Bigram(word[0], word[1])
    trigram = Trigram(word[0], word[1], word[2])
    return (bigram, trigram, float(probability))

def parse_model():
    language_model = SampleLanguageModel(defaultdict(lambda: {}))

    with open(SAMPLE_MODEL_FILENAME, 'r') as input:
        for line in input.readlines():
            (bigram, trigram, probability) = parse_line(line)

            # get existing bigram distribution if available
            bigram_distribution = language_model.distribution_map[bigram]
            if not bigram_distribution:
                bigram_distribution = BigramDistribution(bigram, defaultdict(lambda: 0))
            
            bigram_distribution.dist[trigram] = probability
            language_model.distribution_map[bigram] = bigram_distribution

    return language_model

sample_model = parse_model()
sample_model.validate()

# start_bigram = sample_model.generate_start()
# output = start_bigram.end # Ignore the "#" character in the output

# while len(output) < 300:
#     next_trigram = sample_model.generate_next(start_bigram)

#     if not next_trigram:
#         start_bigram = sample_model.generate_start()
#         output += start_bigram.end # Ignore the "#" character in the output
#         continue

#     if next_trigram.end != "#":
#         output += next_trigram.end
#     start_bigram = Bigram(next_trigram.middle, next_trigram.end)

# print(output)
