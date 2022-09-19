"""Main module."""


def lowercase_input(sentence: str) -> str:
    """Return a copy of a string converted to lowercase.

    Args:
        sentence: Sentence to be lowered cased.

    Returns:
        Lowercased input.

    Demo doctest:

    >>> lowercase_input('My name is Jose')
    'my name is jose'
    """
    return sentence.lower()
