"""
Utility methods. Should not be imported from outside of :module:`configlib`
"""

import re
from typing import List


def parse_case(any_case: str) -> List[str]:
    """
    parses a multiword string from cases like PascalCase or snake_case

    :param any_case: the multi-word string
    :return: the words lowercased as an array
    """
    if '_' in any_case:
        return any_case.lower().split('_')
    if '-' in any_case:
        return any_case.lower().split('-')
    return [word.lower() for word in re.split('(?<=[a-z0-9])(?=[A-Z])', any_case)]


def snake_case(any_case: str) -> str:
    """
    parses a multiword string from cases like PascalCase or snake_case

    :param any_case: the multi-word string
    :return: the words in snake_case
    """
    return '_'.join(parse_case(any_case))


def pascal_case(any_case: str) -> str:
    """
    parses a multiword string from cases like PascalCase or snake_case

    :param any_case: the multi-word string
    :return: the words in PascalCase
    """
    return ''.join(word.capitalize() for word in parse_case(any_case))
