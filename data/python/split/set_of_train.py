def generate_character_set(input_filename, output_filename):
    """
    Reads a file character by character and generates a set of all unique characters.
    Writes the resulting set to an output file.
    
    Args:
        input_filename (str): Path to the input file to read
        output_filename (str): Path to the output file to write the character set
    
    Returns:
        set: The set of unique characters found in the input file
    """
    # Initialize an empty set to store unique characters
    char_set = set()
    
    try:
        # Read the input file character by character
        with open(input_filename, 'r', encoding='utf-8') as infile:
            while True:
                char = infile.read(1)
                if not char:  # End of file
                    break
                char_set.add(char)
        
        # Write the character set to the output file
        with open(output_filename, 'w+', encoding='utf-8') as outfile:
            # Convert set to sorted list for nicer output
            sorted_chars = sorted(char_set)
            # Write each character on a new line with its representation
            for char in sorted_chars:
                outfile.write(f"{char} (ASCII: {ord(char)})\n")
        
        return char_set
    
    except FileNotFoundError:
        print(f"Error: Could not find the input file '{input_filename}'")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Replace these with your actual file paths
    input_file = "/Users/ramjanarthan/Desktop/UoE/projects/kite/data/c++/split/train"
    output_file = "character_set.txt"
    
    char_set = generate_character_set(input_file, output_file)
    
    if char_set is not None:
        print(f"Found {len(char_set)} unique characters")
        print(f"Character set has been written to {output_file}")