import hashlib
from collections import Counter

def analyze_string(value: str):
    """Analyze a string and return its computed properties."""
    value = value.strip()
    sha256_hash = hashlib.sha256(value.encode()).hexdigest()
    length = len(value)
    is_palindrome = value.lower() == value[::-1].lower()
    unique_characters = len(set(value))
    word_count = len(value.split())
    character_frequency_map = dict(Counter(value))

    return {
        "sha256_hash": sha256_hash,
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_characters": unique_characters,
        "word_count": word_count,
        "character_frequency_map": character_frequency_map,
    }
