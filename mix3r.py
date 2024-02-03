#!/usr/bin/env python3
"""
mix3r.py - Mixes wordlists into common patterns that have been seen in real-world pentests.
By: sc1341
Last updated: February 2, 2024
"""

import sys
import random
import string
import os

separators = ['-','.',',','*', '_', '=', '+', "@", '?','|']
special_chars = ['!','@','#','$','%','^','&','*','(',')','_','-','+','=','`','~', '{', '}','|', '?', '<', '>', ':', ';']

def random_case(s):
    return ''.join(random.choice([str.upper, str.lower])(ch) for ch in s)

def simplified_leet_speak(word) -> str:
    """
    Convert a word into simplified leet speak.

    Args:
        word (str): The word to convert.

    Returns:
        str: The word converted into simplified leet speak.

    """
    leet_dict = {
        'a': ['@', '4'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['5', '$'],
        'b': ['8', '|3'],
        'g': ['9', '6'],
        'l': ['1', '|_'],
        't': ['7', '+'],
        'z': ['2']
    }

    def generate_variations(char):
        """
        Generate variations of a character using leet_dict.

        Args:
            char (str): The character to generate variations for.

        Returns:
            list: A list of variations of the character. If the character is not found in leet_dict,
                  the list will contain only the original character.

        """
        return leet_dict.get(char.lower(), [char])

    variations = [generate_variations(char) for char in word]
    
    def combine_variations(variations, index=0, current=''):
        if index == len(variations):
            print(current)
        else:
            for variation in variations[index]:
                combine_variations(variations, index + 1, current + variation)

    combine_variations(variations)


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
                print_if_not_empty(line + str(random.randint(1, 100)))  # Random number at end
                print_if_not_empty(''.join(ch for ch in line if ch.lower() not in 'bcdfghjklmnpqrstvwxyz'))  # No consonants
                print_if_not_empty(line[2:] + line[:2])  # Rotate by 2
                guess_word_boundary_capitalize(line)  # Guess word boundary and capitalize
                simplified_leet_speak(line) # Leet speak
                if ' ' in line:
                    for sep in separators:
                        print_if_not_empty(line.replace(' ', sep))
                # capitalize_range 0 - i
                for i in range(0, 8):
                     print_if_not_empty(capitalize_range(line, 0, i))

def print_if_not_empty(s, min_len=3, max_len=100) -> None:
    """
    Print the string s to stdout if it is not empty and meets the length criteria.

    Args:
        s (str): The string to be printed.
        min_len (int, optional): The minimum length of the string. Defaults to 3.
        max_len (int, optional): The maximum length of the string. Defaults to 100.
    """
    if len(s) > max_len or len(s) < min_len:
        return
    if "$HEX[" in s and "]" in s: # avoid the HEX values completely that sometimes come out.  
        return
    if s.strip():
        print(s)

def guess_word_boundary_capitalize(s) -> None:
    """
    Guesses a word boundary from the input and capitalizes it in several iterations. For example, hotcrossbuns = hotCrossbuns, hotcRossbuns, etc.

    Parameters:
    - s: The input string to guess the word boundary and capitalize it.

    Returns:
    - None
    """
    for avg_word_length in range(2, 12):  # We will guess with avg_word_length from range
        if len(s) <= avg_word_length:
            print_if_not_empty(s.capitalize())
        else:
            parts = [s[i:i+avg_word_length].capitalize() for i in range(0, len(s), avg_word_length)]
            print_if_not_empty(''.join(parts))


def capitalize_range(word, start, end) -> str:
    """
    Capitalizes a specific range of characters in a word.

    Args:
        word (str): The word to be capitalized.
        start (int): The starting index of the range.
        end (int): The ending index of the range.

    Returns:
        str: The word with the specified range of characters capitalized.
    """
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
            Output is sent to stdout. You can redirect it to a file or pipe it directly into tools like HashCat.
            This is designed to be used in conjunction with a hashcat rule set, such as OneRuleToRuleThemAll to ensure enough input is given to HashCat. (https://github.com/NotSoSecure/password_cracking_rules)
        """)
        sys.exit()
        
    if os.path.isdir(sys.argv[1]):
        for file in os.listdir(sys.argv[1]):
            process_words(os.path.join(sys.argv[1], file))
    else:
        process_words(sys.argv[1])
