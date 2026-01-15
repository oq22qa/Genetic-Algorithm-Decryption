"""
Rasa Khosrowshahli
June 11 2025

This module contains methods related to evaluating a chromosome in the GA

Was written as part of assignment 1 for COSC 3P71 in Spring 2025
"""

import random
import string
import numpy as np
import re


def decrypt(k: str, t: str) -> str:
    """Decrypt the text (t) using key (k)

    Args:
        k (str): The key to use for decryption
        t (str): The encrypted text to decrypt

    Returns:
        str: The decrypted text
    """

    # Sanitize the cipher and the key
    cipher = t.lower()
    cipher = re.sub(r'[^a-z]', '', cipher)
    cipher = re.sub(r'\s', '', cipher)

    ke = k.lower()
    ke = re.sub(r'[^a-z]', '', ke)
    ke = re.sub(r'\s', '', ke)

    # Convert key to numpy array of integers (a=0, b=1, ..., z=25)
    key = np.array([ord(c) - 97 for c in ke], dtype=int)

    # Run the decryption
    plain = ""
    key_ptr = 0

    for i in range(len(cipher)):
        key_char = 0
        if len(key) > 0:
            # Ignore any value not in the expected range
            while key[key_ptr] > 25 or key[key_ptr] < 0:
                key_ptr = (key_ptr + 1) % len(key)
            key_char = key[key_ptr]
            key_ptr = (key_ptr + 1) % len(key)

        # Decrypt character using modular arithmetic
        decrypted_char = chr(((ord(cipher[i]) - 97 + 26 - key_char) % 26) + 97)
        plain += decrypted_char

    return plain

def encrypt(k, t):
    """Encrypt text (t) using the provided key (k) -- can use this for testing if needed

    Args:
        k (str): The key to use for encryption
        t (str): The plain text to encrypt

    Returns:
        str: The encrypted text
    """
    # Sanitize the plain text and the key
    plain = t.lower()
    plain = re.sub(r'[^a-z]', '', plain)
    plain = re.sub(r'\s', '', plain)
    cipher = ""

    ke = k.lower()
    ke = re.sub(r'[^a-z]', '', ke)
    ke = re.sub(r'\s', '', ke)

    # Convert key to numpy array of integers (a=0, b=1, ..., z=25)
    key = np.array([ord(c) - 97 for c in ke], dtype=int)

    # Encrypt the text
    key_ptr = 0
    for i in range(len(plain)):
        key_char = 0
        if len(key) > 0:
            # Ignore any value not in the expected range
            while key[key_ptr] > 25 or key[key_ptr] < 0:
                key_ptr = (key_ptr + 1) % len(key)
            key_char = key[key_ptr]
            key_ptr = (key_ptr + 1) % len(key)

        # Encrypt character using modular arithmetic
        encrypted_char = chr(((ord(plain[i]) - 97 + key_char) % 26) + 97)
        cipher += encrypted_char

    return cipher


def fitness(k, t):
    """
    This is a very simple fitness function based on the expected frequency of each letter in english
    There is lots of room for improvement in this function.

    Args:
        k (str): The key to use for decryption
        t (str): The encrypted text to decrypt

    Returns:
        float: The fitness score to be minimized
    """
    # The expected frequency of each character in english language text according to
    # http://practicalcryptography.com/cryptanalysis/letter-frequencies-various-languages/english-letter-frequencies/
    expected_frequencies = np.array([
        0.085,   # Expected frequency of a
        0.016,   # Expected frequency of b
        0.0316,  # Expected frequency of c
        0.0387,  # Expected frequency of d
        0.121,   # Expected frequency of e
        0.0218,  # Expected frequency of f
        0.0209,  # Expected frequency of g
        0.0496,  # Expected frequency of h
        0.0733,  # Expected frequency of i
        0.0022,  # Expected frequency of j
        0.0081,  # Expected frequency of k
        0.0421,  # Expected frequency of l
        0.0253,  # Expected frequency of m
        0.0717,  # Expected frequency of n
        0.0747,  # Expected frequency of o
        0.0207,  # Expected frequency of p
        0.001,   # Expected frequency of q
        0.0633,  # Expected frequency of r
        0.0673,  # Expected frequency of s
        0.0894,  # Expected frequency of t
        0.0268,  # Expected frequency of u
        0.0106,  # Expected frequency of v
        0.0183,  # Expected frequency of w
        0.0019,  # Expected frequency of x
        0.0172,  # Expected frequency of y
        0.0011   # Expected frequency of z
    ])

    # Sanitize the cipher text and key
    d = t.lower()
    d = re.sub(r'[^a-z]', '', d)
    d = re.sub(r'\s', '', d)

    # Convert cipher text to numpy array of integers
    cipher = np.array([ord(c) - 97 for c in d], dtype=int)

    ke = k.lower()
    ke = re.sub(r'[^a-z]', '', ke)
    ke = re.sub(r'\s', '', ke)

    # Convert key to numpy array of integers
    key = np.array([ord(c) - 97 for c in ke], dtype=int)

    # Initialize character counts array
    char_counts = np.zeros(26, dtype=int)

    # Decrypt each character
    plain = np.zeros(len(cipher), dtype=int)
    key_ptr = 0

    for i in range(len(cipher)):
        key_char = 0
        if len(key) > 0:
            # Ignore any value not in the expected range
            while key[key_ptr] > 25 or key[key_ptr] < 0:
                key_ptr = (key_ptr + 1) % len(key)
            key_char = key[key_ptr]
            key_ptr = (key_ptr + 1) % len(key)

        plain[i] = (26 + cipher[i] - key_char) % 26

    # Count the occurrences of each character using numpy
    for char_val in plain:
        char_counts[char_val] += 1

    # Calculate the total difference between the expected frequencies and the actual frequencies
    actual_frequencies = char_counts.astype(float) / len(plain)
    score = np.sum(np.abs(actual_frequencies - expected_frequencies))

    return score

def read_encrypted_data(filename: str) -> tuple[int, str]:
    """Read encrypted data from file, returning key length and cipher text

    Args:
        filename (str): The name of the file to read

    Returns:
        tuple[int, str]: The key length and cipher text
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    # First line contains the key length
    key_length = int(lines[0].strip())

    # Rest of the lines contain the encrypted text
    cipher_text = ''.join(line.strip() for line in lines[1:])

    return key_length, cipher_text

def evaluate_key_on_data(key: str, cipher_text: str) -> tuple[float, str]:
    """Evaluate a given key on a specific data file

    Args:
        key (str): The key to evaluate
        cipher_text (str): The cipher text to evaluate

    Returns:
        tuple[float, str]: The fitness score and the decrypted text
    """

    key_length = len(key)

    print(f"\n--- Evaluating key '{key}' ---")
    print(f"Key length: {key_length}")
    print(f"Cipher text length: {len(cipher_text)}")

    # Calculate fitness score
    score = fitness(key, cipher_text)
    print(f"Fitness score: {score:.6f}")

    # Show a sample of the decrypted text
    decrypted = decrypt(key, cipher_text)
    print(f"First 100 characters of decrypted text: {decrypted[:100]}")

    return score, decrypted

def test_random_keys(data_files: list[str], trials: int = 10) -> None:
    """Test keys of the expected lengths for each data file

    Args:
        data_files (list[str]): The data files to test
        trials (int): The number of trials to run for each data file

    Returns:
        None
    """
    print(f"\n{'='*60}")
    print("TESTING KEYS USING DATA FILES: " + str(data_files))
    print(f"{'='*60}")

    valid_chars = string.ascii_lowercase

    for data_file in data_files:
        print(f"\n--- Testing {data_file} ---")

        # Read expected key lengths
        key_length, cipher_text = read_encrypted_data(data_file)

        best_score = float('inf')
        best_key = ""
        best_decrypted = ""

        for i in range(trials):
            key = ''.join(random.choice(valid_chars) for _ in range(key_length))

            score, decrypted = evaluate_key_on_data(key, cipher_text)
            if score < best_score:
                best_score = score
                best_key = key
                best_decrypted = decrypted

        print(f"\nBest key for {data_file}: '{best_key}' (score: {best_score:.6f})")
        print(f"Decrypted text sample: {best_decrypted[:200]}...")


# Example usage and testing
if __name__ == "__main__":
    # Test the data using random keys
    test_random_keys(["Data1.txt", "Data2.txt"], trials=10)
