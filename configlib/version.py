from dataclasses import dataclass


@dataclass
class VersionInfo:
    major: int
    minor: int
    build: int
    level: str
    serial: int

    def __str__(self):
        return '{major}.{minor}.{build}{level}{serial}'.format(**self.__dict__)


version = VersionInfo(1, 0, 0, 'a', 0)
