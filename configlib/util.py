import re
from typing import List


def parse_case(any_case: str) -> List[str]:
    if '_' in any_case:
        return any_case.lower().split('_')
    if '-' in any_case:
        return any_case.lower().split('-')
    return [word.lower() for word in re.split('(?<=[a-z0-9])(?=[A-Z])', any_case)]


def snake_case(any_case: str) -> str:
    return '_'.join(parse_case(any_case))


def pascal_case(any_case: str) -> str:
    return ''.join(word.capitalize() for word in parse_case(any_case))
