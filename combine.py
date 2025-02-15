def combine_character_sets(file1_path, file2_path, output_path):
    """
    Combines character sets from two files and writes the unified set to a new file.
    Expects files in the format: "char (ASCII: number)"
    
    Args:
        file1_path (str): Path to first character set file
        file2_path (str): Path to second character set file
        output_path (str): Path to output combined character set file
    
    Returns:
        set: Combined set of characters
    """
    combined_chars = set()
    
    # Helper function to extract characters from a file
    def read_chars_from_file(filepath):
        chars = set()
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():  # Skip empty lines
                        # Extract the character (first character of the line)
                        char = line.strip()[0]
                        chars.add(char)
        except Exception as e:
            print(f"Error reading {filepath}: {str(e)}")
        return chars
    
    # Read both files and combine the sets
    set1 = read_chars_from_file(file1_path)
    set2 = read_chars_from_file(file2_path)
    combined_chars = set1.union(set2)
    
    # Write the combined set to output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for char in sorted(combined_chars):
                f.write(f"{char} (ASCII: {ord(char)})\n")
        print(f"Combined character set written to {output_path}")
    except Exception as e:
        print(f"Error writing to {output_path}: {str(e)}")
    
    return combined_chars

def initialize_char_set_from_file(filepath):
    """
    Initializes a set of characters from a file in the format "char (ASCII: number)".
    
    Args:
        filepath (str): Path to the character set file
    
    Returns:
        set: Set of characters read from the file
    """
    char_set = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():  # Skip empty lines
                    # Extract the character (first character of the line)
                    char = line.strip()[0]
                    char_set.add(char)
        return char_set
    except Exception as e:
        print(f"Error reading character set from {filepath}: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Example file paths
    file1 = "character_set_1.txt"
    file2 = "character_set.txt"
    combined_file = "combined_charset.txt"
    
    # Combine the character sets
    combined_chars = combine_character_sets(file1, file2, combined_file)
    print(f"Combined set contains {len(combined_chars)} characters")
    
    # Initialize a set from the combined file
    char_set = initialize_char_set_from_file(combined_file)
    if char_set:
        print(f"Successfully initialized character set with {len(char_set)} characters")
        print("Sample of characters:", ''.join(sorted(list(char_set))[:10]), "...")