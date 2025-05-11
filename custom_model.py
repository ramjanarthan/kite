from counts import *
from constants import *
from primitives import *
from vocabulary import *
import random
from generator import sample
from preprocessor import FilePreprocessor
import math
import pickle
import os
import sys
import datetime


class CustomLanguageModel:
    """For a given vocabulary and training input, contains all the trigram distributions over that set of bigrams"""
    DEBUG_MODE = False

    def __init__(self, filename=None, alpha=0.63, model_file=None) -> None:
        self.distribution_map = defaultdict(self.default_dict_factory)
        if model_file:
            self.load_model(model_file)
        elif filename:
            self._compute_model(filename, alpha)

    def default_dict_factory(self):
        return {}
    
    def default_dict_empty_count_factory(self):
        return 0

    def _compute_model(self, filename, alpha):
        """ For a given filename as input, compute trigram probabilities"""
        bigram_counts = calculate_bigram_counts(filename)
        trigram_counts = calculate_trigram_counts(filename)
        vocabulary = generate_trigram_vocab()
        vocab_size = len(generate_base_vocab())

        for trigram in vocabulary:
            bigram = trigram.history()
            bigram_count = bigram_counts[bigram]
            trigram_count = trigram_counts[trigram]
            
            # Smoothing
            probability = (trigram_count * 1.0 + alpha) / (bigram_count + alpha * vocab_size)

            bigram_distribution = self.distribution_map[bigram]
            if not bigram_distribution:
                bigram_distribution = BigramDistribution(bigram, defaultdict(self.default_dict_empty_count_factory))
            
            bigram_distribution.dist[trigram] = probability
            self.distribution_map[bigram] = bigram_distribution

    def save_model(self, model_file):
        """Save the model to a file"""
        with open(model_file, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_model(model_file):
        """Load the model from a file"""
        with open(model_file, 'rb') as f:
            return pickle.load(f)

    def generate_next(self, context): 
        """Given a bigram 'context', generate a possible 'trigram' that is most likely that this bigram prefixes"""

        bigram_dist = self.distribution_map[context]

        if not bigram_dist:
            # For example, if context == Bigram('.', "#")
            return None
        
        sampled_trigram = sample(bigram_dist.dist)
        return sampled_trigram
    
    def generate_start(self, start_symbol = None) -> Bigram:
        """Method to sample from all possible start bigrams"""

        if start_symbol:
            return start_symbol

        return random.choice(list(self.distribution_map.keys()))

    def validate(self):
        """For a given bigram_distribution, we expect the sum of all trigram probabilities to sum to one"""
        for (key, distribution) in sorted(self.distribution_map.items()):
            sum = 0
            for (trigram, probability) in sorted(distribution.dist.items()):
                sum += probability
                if CustomLanguageModel.DEBUG_MODE:
                    print(f"sum {sum} probability: {probability} trigram: {trigram}")
            
            if abs(1 - sum) > 0.001:
                if CustomLanguageModel.DEBUG_MODE:
                    print(f"Error with sum: {sum} for key: {key}")
                raise Exception(f"Validation failed for model. Erroneous bigram distribution: {key}")
            else:
                if CustomLanguageModel.DEBUG_MODE:
                    print(f"Valid for: {key}")
            
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

        # 7. delete processed file
        os.remove(new_filename)
        return perplexity
    
    def generate_output_sequence(self, length, seed = None) -> str:
        start_bigram = self.generate_start(seed)
        output = self._sanitise_bigram(start_bigram)

        while len(output) <= length:
            next_trigram = self.generate_next(start_bigram)

            if not next_trigram:
                start_bigram = self.generate_start(seed)
                output += self._sanitise_bigram(start_bigram)
                continue

            output += self._sanitise_character(next_trigram.end)

            start_bigram = Bigram(next_trigram.middle, next_trigram.end)
        return output
    
    def _sanitise_bigram(self, bigram):
        return self._sanitise_character(bigram.start) + self._sanitise_character(bigram.end)
    
    def _sanitise_character(self, char):
        if char == space_character:
            return ' '
        elif char == tab_character:
            return '\t'
        elif char == new_line_character:
            return '\n'
        elif char == number_mask_character:
            return random.choice(numeric_characters)
        else:
            return char
        
    def debug_print(self, model_name):
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create debug directory with timestamp
        debug_dir = f"debug_logs_{timestamp_str}"
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
        
        # Sanitize model_name for use in filename (e.g., handle paths, spaces)
        base_model_name = os.path.basename(model_name)
        safe_model_name_prefix = base_model_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
        
        debug_filename = os.path.join(debug_dir, f"{safe_model_name_prefix}_memory_debug.txt")

        try:
            with open(debug_filename, 'w') as f:
                f.write(f"Memory Debug Report for Model: {model_name}\n")
                f.write(f"Timestamp: {timestamp_str}\n")
                f.write("==================================================\n\n")

                # Print lengths of keys
                f.write("Key Lengths:\n")
                f.write("----------------------------------------\n")
                if self.distribution_map:
                    sample_bigram = next(iter(self.distribution_map.values()))
                    f.write(f"Length of distribution_map keys: {len(self.distribution_map)}\n")
                    f.write(f"Length of BigramDistribution keys: {len(sample_bigram.dist)}\n")
                f.write("\n")

                # 1. Whole class memory footprint
                f.write("1. Overall Class Memory Footprint:\n")
                f.write("----------------------------------------\n")
                class_size = sys.getsizeof(self)
                f.write(f"Total size of CustomLanguageModel instance: {class_size} bytes\n")
                f.write(f"Size of distribution_map attribute: {sys.getsizeof(self.distribution_map)} bytes\n")
                f.write("\n")

                # 2. Sample BigramDistribution analysis
                f.write("2. Sample BigramDistribution Analysis:\n")
                f.write("----------------------------------------\n")
                if self.distribution_map:
                    # Get a sample bigram distribution
                    sample_bigram = next(iter(self.distribution_map.values()))
                    sample_size = sys.getsizeof(sample_bigram)
                    f.write(f"Size of one BigramDistribution object: {sample_size} bytes\n")
                    f.write(f"Size of BigramDistribution's dist dictionary: {sys.getsizeof(sample_bigram.dist)} bytes\n")
                    f.write("\n")

                    # 3. Sample entry analysis
                    f.write("3. Sample Entry Analysis:\n")
                    f.write("----------------------------------------\n")
                    if sample_bigram.dist:
                        sample_entry = next(iter(sample_bigram.dist.items()))
                        entry_size = sys.getsizeof(sample_entry[0]) + sys.getsizeof(sample_entry[1])
                        f.write(f"Size of one entry (trigram + probability): {entry_size} bytes\n")
                        f.write(f"Size of trigram key: {sys.getsizeof(sample_entry[0])} bytes\n")
                        f.write(f"Size of probability value: {sys.getsizeof(sample_entry[1])} bytes\n")
                        f.write("\n")

                # 4. Distribution counts
                f.write("4. Distribution Statistics:\n")
                f.write("----------------------------------------\n")
                num_bigrams = len(self.distribution_map)
                f.write(f"Total number of bigram distributions: {num_bigrams}\n")
                
                # 5. Entry counts per distribution
                if self.distribution_map:
                    entry_counts = [len(dist.dist) for dist in self.distribution_map.values()]
                    avg_entries = sum(entry_counts) / len(entry_counts) if entry_counts else 0
                    max_entries = max(entry_counts) if entry_counts else 0
                    min_entries = min(entry_counts) if entry_counts else 0
                    f.write(f"Average entries per distribution: {avg_entries:.2f}\n")
                    f.write(f"Maximum entries in a distribution: {max_entries}\n")
                    f.write(f"Minimum entries in a distribution: {min_entries}\n")
                    f.write("\n")

                # Memory estimation
                f.write("5. Total Memory Estimation:\n")
                f.write("----------------------------------------\n")
                if self.distribution_map:
                    total_entries = sum(len(dist.dist) for dist in self.distribution_map.values())
                    estimated_memory = (
                        class_size +  # Base class size
                        sys.getsizeof(self.distribution_map) +  # Distribution map overhead
                        (sample_size * num_bigrams) +  # All BigramDistribution objects
                        (entry_size * total_entries)  # All entries
                    )
                    f.write(f"Estimated total memory footprint: {estimated_memory} bytes\n")
                    f.write(f"Number of total trigram entries: {total_entries}\n")
                    f.write(f"Average memory per entry: {estimated_memory/total_entries:.2f} bytes\n")
                
                f.write("\n==================================================\n")
                report_path = os.path.abspath(debug_filename)
                f.write(f"Debug report saved to: {report_path}\n")

        except IOError as e:
            print(f"Error writing memory debug report for model '{model_name}' to file '{debug_filename}': {e}")
