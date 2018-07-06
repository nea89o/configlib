import json
from abc import abstractmethod, ABC
from typing import TypeVar, Type, Union, AnyStr, TextIO

_T = TypeVar('_T', bound='Config')


class InvalidConfigTypingException(Exception):
    pass


class ConfigValueMissingException(Exception):
    pass


class Config(ABC):

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def parse_dict(cls: Type[_T], data: dict) -> _T:
        pass

    @classmethod
    def load(cls: Type[_T], file: Union[AnyStr, TextIO]) -> _T:
        if hasattr(file, 'read'):
            return cls.loads(file.read())
        with open(file) as fp:
            return cls.load(fp)

    @classmethod
    def loads(cls: Type[_T], text: str) -> _T:
        return cls.parse_dict(json.loads(text))

    @classmethod
    def get_instance(cls: Type[_T]) -> _T:
        return cls
