from typing import TypeVar, Type, Dict, List

from .model import Config, ConfigValueMissingException, InvalidConfigTypingException
from .util import snake_case

_T = TypeVar('_T', bound=Config)

_T0 = TypeVar('_T0')


def parse_list_impl(cls: Type[_T0], data, path=''):
    lis = []
    for i, item in enumerate(data):
        list.append(parse_single_item(cls, item, path + '[' + str(i) + ']'))
    return lis


def parse_obj_impl(cls: Type[_T0], data, path='Config') -> _T0:
    obj = cls()
    annotations: Dict[str, Type] = obj.__annotations__
    for key, val_type in annotations.items():
        if key not in data.keys():
            raise ConfigValueMissingException(path + key)
        val = data[key]
        setattr(obj, key, parse_single_item(val_type, val, path + '.' + key))
    return obj


def parse_dict_impl(val_type: Type[_T0], val, path) -> _T0:
    dic = {}
    for key, value in val.items():
        dic[key] = parse_single_item(val_type, value, path + '[' + repr(key) + ']')
    return dic


def parse_single_item(val_type: Type[_T0], val, path) -> _T0:
    if issubclass(val_type, (str, int, float)):
        return val
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
    @classmethod
    def get_name(cls) -> str:
        return snake_case(cls.__name__).upper()

    @classmethod
    def parse_dict(cls: Type[_T], data: dict) -> _T:
        return parse_obj_impl(cls, data)
