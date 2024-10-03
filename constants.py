# Allowed characters based on the ASCII table
numeric_characters = list(map(chr, range(48, 58)))
allowed_characters = list(map(chr,range(97, 123))) + [" ", "."]
start_of_line_character = "^"
end_of_line_character = "$"
number_mask_character = "0"
