def search4vowels(phrase: str) -> str:
    """Return vowels"""
    vowels = set("aeiou")
    return vowels.intersection(set(phrase))


def search4letters(phrase: str, letters: str = "aeiou") -> str:
    return set(letters).intersection(set(phrase))
