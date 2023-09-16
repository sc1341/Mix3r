#!/usr/bin/env python3
"""
mix3r.py - Mixes wordlists into common patterns

"""
import sys
import random
import string
import os

separators = ['-','.',',','*', '_', '=', '+', "@"]
special_chars = ['!','@','#','$','%','^','&','*','(',')','_','-','+','=','`','~', '{', '}','|', '?', '<', '>', ':', ';']

def random_case(s):
    return ''.join(random.choice([str.upper, str.lower])(ch) for ch in s)


def leet_speak(s):
    leet_dict = {
        'a': '4', 'A': '4',
        'e': '3', 'E': '3',
        'i': '1', 'I': '1',
        'o': '0', 'O': '0',
        's': '5', 'S': '5',
        't': '7', 'T': '7',
    }
    return ''.join(leet_dict.get(ch, ch) for ch in s)


def process_words(file):
    with open(file, 'r', errors='ignore') as f:
        for line in f:
            line = line.strip('\n')
            line = line.strip(' ') # get the extra space off the end
            if line:  # Check if line is not empty
                print_if_not_empty(line)  # Original
                print_if_not_empty(' ' + line) # space before
                print_if_not_empty(line + ' ') # space after
                for year in range(1970, 2028): # YEARS
                     print_if_not_empty(str(year) + line)
                     print_if_not_empty(line + str(year))
                print_if_not_empty(line.upper())  # Capitalize
                print_if_not_empty(line.lower())  # Lowercase
                print_if_not_empty(line.capitalize())  # Capitalize first letter
                print_if_not_empty(random_case(line)) # random case 
                print_if_not_empty(line[::-1])  # Reverse
                print_if_not_empty(''.join(ch.upper() if ch.islower() else ch.lower() for ch in line))
                wrapped_lines = [char*n + line + char*n for char in special_chars for n in range(1, 3)]  # Adjust range to increase the number of wrapped characters
                for wrapped in wrapped_lines:
                     print_if_not_empty(wrapped) # print out results of previous operation 
                print_if_not_empty(''.join(ch for ch in line if ch not in 'aeiouAEIOU'))  # No vowels
                print_if_not_empty(''.join(ch * 2 for ch in line))  # Double letters
                print_if_not_empty(''.join(ch + random.choice(string.ascii_letters) for ch in line))  # Random char between
                print_if_not_empty(line[::-1].upper())  # Reverse Capitalized
                print_if_not_empty(line.swapcase())  # Swap case
                print_if_not_empty(line * 2)  # Repeat line
                print_if_not_empty(leet_speak(line))  # Leet speak
                print_if_not_empty(line + str(random.randint(1, 100)))  # Random number at end
                print_if_not_empty(''.join(ch for ch in line if ch.lower() not in 'bcdfghjklmnpqrstvwxyz'))  # No consonants
                print_if_not_empty(line[2:] + line[:2])  # Rotate by 2
                guess_word_boundary_capitalize(line)  # Guess word boundary and capitalize
                # Add different separators if necessary 
                if ' ' in line:
                    for sep in separators:
                        print_if_not_empty(line.replace(' ', sep))
                # capitalize_range 0 - i
                for i in range(0, 8):
                     print_if_not_empty(capitalize_range(line, 0, i))

def print_if_not_empty(s, min_len=0, max_len=100):
    # Print s if it is not an empty string
    if len(s) > max_len or len(s) < min_len:
        return
    if "$HEX[" in s and "]" in s: # avoid the HEX values completely 
        return
    if s.strip():
        print(s)

def guess_word_boundary_capitalize(s):
    # Guess word boundary and capitalize
    for avg_word_length in range(2, 10):  # We will guess with avg_word_length from range
        if len(s) <= avg_word_length:
            print_if_not_empty(s.capitalize())
        else:
            parts = [s[i:i+avg_word_length].capitalize() for i in range(0, len(s), avg_word_length)]
            print_if_not_empty(''.join(parts))

def capitalize_range(word, start, end):
    # inclusive? 
    if len(word) < end:
        return word
    return word[start:end+1].upper() + word[end+1::]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("""mix3r.py: A Powerful Wordlist Manipulator

Description:
    mix3r.py is designed to take wordlists and apply various string manipulations 
    to generate potential password candidates. Whether you're conducting a password 
    cracking exercise or just want to see the myriad ways a string can be transformed, 
    mix3r.py provides a comprehensive set of operations.

Features:
    1. Basic transformations: upper case, lower case, capitalize, reverse.
    2. Advanced manipulations: leet speak conversion, random case application, vowel/consonant stripping.
    3. Numeric augmentations: prepend/append years, append random numbers.
    4. Special character operations: wrap strings with special characters, replace spaces with separators.
    5. Predictive manipulations: guessed word boundary capitalization, pattern-based string repetition.

Usage:
    python3 mix3r.py [wordlist directory or wordlist]

Note:
    Output is sent to stdout. You can redirect it to a file or pipe it directly into tools like hashcat.
    This is designed to be used in conjunction with a hashcat rule set, such as OneRuleToRuleThemAll. (https://github.com/NotSoSecure/password_cracking_rules)
""")
        sys.exit()
    if os.path.isdir(sys.argv[1]):
        for file in os.listdir(sys.argv[1]):
            process_words(sys.argv[1] + file)
    else:
        process_words(sys.argv[1])
