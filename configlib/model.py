"""
Abstract models and classes for the config

"""

import json
import os
from abc import abstractmethod, ABC
from typing import Type, Union, AnyStr, TextIO

from configlib.util import snake_case


class InvalidConfigEscapeException(Exception):
    """
    Some config uses an invalid escape like `$invalidescapecode:argument`
    """


class InvalidConfigTypingException(Exception):
    """
    The typing found in the given class is missing arguments.
    Example:

    >>> import typing
    >>> someting: typing.List[str, int]

    is illegal since :class:`typing.List` only takes one argument.
    """


class ConfigValueMissingException(Exception):
    """
    The given config file is missing an argument
    """


class Config(ABC):
    """
    Base class for a Config. Do NOT extend this. use :class:`configlib.BaseConfig` instead.

    """

    @classmethod
    @abstractmethod
    def get_name(cls) -> str:
        """
        Get the name for a config

        :return: the name
        """

    @classmethod
    @abstractmethod
    def parse_dict(cls: Type['Config'], data: dict) -> 'Config':
        """
        For the given data return the config instance.

        :param data: the loaded data dict
        :return: a loaded config
        """

    @classmethod
    def load(cls: Type['Config'], file: Union[AnyStr, TextIO]) -> 'Config':
        """
        Load a specified config file

        :param file: the file object or file path
        :return: the parsed config according to :func:`.parse_dict`
        """
        if hasattr(file, 'read'):
            return cls.loads(file.read())
        with open(file) as file_pointer:
            return cls.load(file_pointer)

    @classmethod
    def loads(cls: Type['Config'], text: str) -> 'Config':
        """
        Load data from text

        :param text: the text data
        :return: the parsed config
        """
        return cls.parse_dict(json.loads(text))

    @classmethod
    def get_instance(cls: Type['Config']) -> 'Config':
        """
        get a Config instance according to the matching environment variable

        :return: the parsed config
        """
        name = os.environ.get(snake_case(cls.get_name()), '').strip()
        return cls.get_instance_for_env(name)

    @classmethod
    def get_instance_for_env(cls: Type['Config'], env: str) -> 'Config':
        """
        get a Config instance for a given environment

        :param env: the wanted environment
        :return: the parsed config
        """
        if env:
            env = '-' + env
        return cls.load('config/' + snake_case(cls.get_name()) + env + '.json')
