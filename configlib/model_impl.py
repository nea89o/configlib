"""
Implementations for the modules of :module:`configlib.model`
"""
import os
from typing import Type, Dict, List

from .model import Config, ConfigValueMissingException, InvalidConfigTypingException, \
    InvalidConfigEscapeException
from .util import snake_case


def parse_list_impl(cls: Type[object], data, path='') -> list:
    """
    parse a list and reinterpret the individual elements according to `cls`

    :param cls: the type of each list element
    :param data: the actual list elements
    :param path: the path inside the config. used for error reporting
    :return: the list with transformed elements.
    """
    lis = []
    for i, item in enumerate(data):
        lis.append(parse_single_item(cls, item, path + '[' + str(i) + ']'))
    return lis


def parse_obj_impl(cls: Type[object], data, path='Config') -> object:
    """
    parse a dict into an object according to `cls`

    :param cls: the type of the resulting object
    :param data: the dict object
    :param path: the path inside the config. used for error reporting
    :return: the parsed object
    """
    obj = cls()
    annotations: Dict[str, Type] = obj.__annotations__
    for key, val_type in annotations.items():
        if key not in data.keys():
            raise ConfigValueMissingException(path + key)
        val = data[key]
        setattr(obj, key, parse_single_item(val_type, val, path + '.' + key))
    return obj


def parse_dict_impl(val_type: Type[object], val, path) -> dict:
    """
    Parse a dict and reinterpret the values according to `val_type`

    :param val_type: the type of the values of the dict
    :param val: the actual dict to be reinterpreted
    :param path: the path inside the config. used for error reporting
    :return: the reinterpreted dict
    """
    dic = {}
    for key, value in val.items():
        dic[key] = parse_single_item(val_type, value, path + '[' + repr(key) + ']')
    return dic


_ESCAPES = {
    'env': os.environ.get,
}


def _resolve_string(val: str):
    if val[0] != '$':
        return val
    if val[1] == '$':
        return val[1:]
    descriptor, arg, *_ = val[1:].split(':', 2) + ['']
    escape = _ESCAPES.get(descriptor)
    if not escape:
        raise InvalidConfigEscapeException(descriptor)
    return escape(arg)


# noinspection PyUnresolvedReferences
def parse_single_item(val_type: Type[object], val, path):
    """
    dynamically parse an item into a dict, list, object or a primitive depending on `val_type`

    :param val_type: the type to be discussed
    :param val: the value to be parsed
    :param path: the path inside the config. used for error reporting
    :return: the parsed something
    """
    if isinstance(val, str):
        if len(val) > 2 and val[0] == '$':
            val = _resolve_string(val)

    if issubclass(val_type, (str, int, float)):
        # noinspection PyArgumentList
        return val_type(val)
    if isinstance(val_type, List):
        if len(val_type.__args__) != 1:
            raise InvalidConfigTypingException(path + ': List must be supplied exactly one type')
        return parse_list_impl(val_type.__args__[0], val, path)
    if isinstance(val_type, Dict):
        if len(val_type.__args__) != 2:
            raise InvalidConfigTypingException(path + ': Dict must be supplied exactly two types')
        if val_type.__args__[0] != str:
            raise InvalidConfigTypingException(path + ': Dict must have `str` as indexing')
        return parse_dict_impl(val_type.__args__[1], val, path)
    return parse_obj_impl(val_type, val, path)


class BaseConfig(Config):
    """
    A :class:`Config` implementation using type hints for parsing.
    """

    @classmethod
    def get_name(cls) -> str:
        return snake_case(cls.__name__).upper()

    @classmethod
    def parse_dict(cls: Type['BaseConfig'], data: dict) -> 'BaseConfig':
        # noinspection PyTypeChecker
        return parse_obj_impl(cls, data)
