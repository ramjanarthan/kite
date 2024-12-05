from counts import *
from constants import *
from primitives import *
import random
from generator import sample
from preprocessor import FilePreprocessor
import math
import numpy as np
import matplotlib.pyplot as plt

class CustomLanugageModel:
    """For a given vocabulary and training input, contains all the trigram distributions over that set of bigrams"""
    DEBUG_MODE = False

    def __init__(self, filename, alpha) -> None:
        self.distribution_map = defaultdict(lambda: {})
        self._compute_model(filename, alpha)

    def _compute_model(self, filename, alpha):
        """ For a given filename as input, compute trigram probabilites"""
        bigram_counts = calculate_bigram_counts(filename)
        trigram_counts = calculate_trigram_counts(filename)
        vocabulary = self.generate_trigram_vocabulary()
        vocab_size = 30 # An appromixation, close to the average (since ^ and & are not legal in all positions in this model)

        for trigram in vocabulary:
            bigram = trigram.history()
            bigram_count = bigram_counts[bigram]
            trigram_count = trigram_counts[trigram]
            
            # Smoothing
            probability = (trigram_count * 1.0 + alpha)/ (bigram_count + alpha * vocab_size)

            bigram_distribution = self.distribution_map[bigram]
            if not bigram_distribution:
                bigram_distribution = BigramDistribution(bigram, defaultdict(lambda: 0))
            
            bigram_distribution.dist[trigram] = probability
            self.distribution_map[bigram] = bigram_distribution

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

        possibilites = [Bigram("^", ' '), Bigram("^", '.'), Bigram('^', '0'), Bigram('^', 'a'), Bigram('^', 'b'), Bigram('^', 'c'), Bigram('^', 'd'), Bigram('^', 'e'), Bigram('^', 'f'), Bigram('^', 'g'), Bigram('^', 'h'), Bigram('^', 'i'), Bigram('^', 'j'), Bigram('^', 'k'), Bigram('^', 'l'), Bigram('^', 'm'), Bigram('^', 'n'), Bigram('^', 'o'), Bigram('^', 'p'), Bigram('^', 'q'), Bigram('^', 'r'), Bigram('^', 's'), Bigram('^', 't'), Bigram('^', 'u'), Bigram('^', 'v'), Bigram('^', 'w'), Bigram('^', 'x'), Bigram('^', 'y'), Bigram('^', 'z')]

        bigrams_missing_in_training = [Bigram("^", ' '), Bigram("^", '^'), Bigram("^", 'x'), Bigram("^", 'z'), Bigram("^", '0')]

        return random.choice(list(set(possibilites) - set(bigrams_missing_in_training)))

    def validate(self):
        """For a given bigram_distribution, we expect the sum of all trigram probabilites to sum to one"""
        for (key, distribution) in sorted(self.distribution_map.items()):
            sum = 0
            for (trigram, probability) in sorted(distribution.dist.items()):
                sum += probability
                if CustomLanugageModel.DEBUG_MODE:
                    print(f"sum { sum} proabbility: {probability} trigram: {trigram}")
            
            if abs(1 - sum) > 0.001:
                if CustomLanugageModel.DEBUG_MODE:
                    print(f"Error with sum: {sum} for key: {key}")
                raise Exception(f"Validation failed for model. Erronous bigram distribution: {key}")
            else:
                if CustomLanugageModel.DEBUG_MODE:
                    print(f"Valid for: {key}")
            
        return True
    
    def generate_trigram_vocabulary(self) -> list[Trigram]:
        all_chars = set(allowed_characters).union(set([start_of_line_character] + [end_of_line_character] + [number_mask_character]))
        vocabulary = []

        for first in all_chars:
            for second in all_chars:
                for third in all_chars:
                    trigram = Trigram(first, second, third)
                    vocabulary += [trigram]
        
        # remove illegal trigrams
        return list(filter(self._helper_filter, vocabulary))
    
    def _helper_filter(self, trigram) -> bool :
        if trigram.start == '$' or trigram.middle == '$':
            return False
        elif trigram.middle == '^' or trigram.end == '^':
            return False
        return True
    
    def compute_perplexity(self, filename):
        # 1. Read in file contents
        file_preprocessor = FilePreprocessor()
        new_filename = f"{filename}_processed"

        # 2. Preprocess file similar to expected vocab
        file_preprocessor.preprocess_file(filename, new_filename)

        # 3. Tokenize as trigrams
        trigram_tokenizer = TrigramTokenizer(new_filename)

        # 4. For each trigram, sum the log P 
        count = 0
        log_sum = 0
        while next_trigram := trigram_tokenizer.next():
            bigram_distribution = self.distribution_map[next_trigram.history()]

            if not bigram_distribution:
                # print(f"Missing bigram: {next_trigram.history}")
                continue
            probability = bigram_distribution.dist[next_trigram]

            if not bigram_distribution or not probability:
                continue
                # raise Exception(f"Error when computing probability for trigram: {next_trigram}")
            
            log_probability = math.log10(probability)
            log_sum += log_probability
            count += 1

        # 5. multiply by -1/count , where count == total number of trigrams
        scaled_log_sum = -1 * log_sum / count

        # 6. raise base of log to value of step 5, to get perplexity
        perplexity = math.pow(10, scaled_log_sum)
        return perplexity
    
    def generate_output_sequence(self, length) -> str:
        start_bigram = self.generate_start()
        output = start_bigram.end # Ingnore the '^' in the output

        while len(output) <= length:
            next_trigram = self.generate_next(start_bigram)

            if not next_trigram:
                start_bigram = self.generate_start()
                output += start_bigram.end  # Ingnore the '^' in the output
                continue

            if next_trigram.end != "$":
                output += next_trigram.end

            start_bigram = Bigram(next_trigram.middle, next_trigram.end)
        return output
   
python_model = CustomLanugageModel(processed_files[0], 0.63)
cpp_model = CustomLanugageModel(processed_files[1], 0.63)

print(f"Perplexity of python: {python_model.compute_perplexity(validation_files[1])}")
print(f"Perplexity of c++: {cpp_model.compute_perplexity(validation_files[1])}")
