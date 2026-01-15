# Cipher Decryption using Genetic Algorithm

## Overview
This program implements a genetic algorithm approach to decrypt text that has been encrypted using a simple substitution cipher. The program uses letter frequency analysis to evaluate potential decryption keys and attempts to find the optimal key through random trials.

## Features
- Encryption and decryption of text using a substitution cipher
- Fitness function based on English letter frequency analysis
- Support for multiple data files with different key lengths
- Random key testing functionality
- Text sanitization and preprocessing

## File Structure
- `evaluation.py`: Main program file containing all the cipher-related functionality
- `Data1.txt`, `Data2.txt`: Sample encrypted data files

## Functions

### Core Functions
1. `decrypt(k: str, t: str) -> str`
   - Decrypts cipher text using a provided key
   - Sanitizes input by removing non-alphabetic characters
   - Returns the decrypted plain text

2. `encrypt(k: str, t: str) -> str`
   - Encrypts plain text using a provided key
   - Sanitizes input by removing non-alphabetic characters
   - Returns the encrypted cipher text

3. `fitness(k: str, t: str) -> float`
   - Evaluates the quality of a decryption key
   - Uses English letter frequency analysis
   - Returns a score (lower is better)

### Utility Functions
1. `read_encrypted_data(filename: str) -> tuple[int, str]`
   - Reads encrypted data from a file
   - Returns key length and cipher text

2. `evaluate_key_on_data(key: str, cipher_text: str) -> tuple[float, str]`
   - Evaluates a key on specific cipher text
   - Returns fitness score and decrypted text

3. `test_random_keys(data_files: list[str], trials: int = 10) -> None`
   - Tests random keys on multiple data files
   - Performs specified number of trials
   - Reports best key and decrypted text

## Usage
1. Prepare your encrypted data file:
   - First line should contain the key length
   - Remaining lines should contain the encrypted text

2. Run the program:
```python
python evaluation.py
```

3. The program will:
   - Test random keys on the provided data files
   - Display the best key found
   - Show a sample of the decrypted text

## Implementation Details
- Uses numpy for efficient array operations
- Implements modular arithmetic for encryption/decryption
- Uses regular expressions for text sanitization
- Based on English letter frequency statistics from practicalcryptography.com

## Notes
- The fitness function is based on a simple letter frequency analysis
- There is room for improvement in the fitness function
- The program currently uses random key generation for testing
- The encryption/decryption process ignores non-alphabetic characters