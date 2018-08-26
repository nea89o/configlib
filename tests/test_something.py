import json
import os
from unittest import TestCase

from configlib.model_impl import BaseConfig


class Yeeah(object):
    a: int


class SomeConfig(BaseConfig):
    something: str
    ye: Yeeah


test_dict = {
    'something': 'hmm',
    'ye': {
        'a': 1
    }
}
env_dict = {
    'something': '$env:ENVVAR',
    'ye': {
        'a': 1
    }
}


def verify_test_dict(conf):
    assert conf.something == 'hmm'
    assert isinstance(conf, SomeConfig)
    assert conf.ye.a == 1
    assert isinstance(conf.ye, Yeeah)


class TestSomething(TestCase):

    def test_yeah(self):
        conf: SomeConfig = SomeConfig.parse_dict(test_dict)
        verify_test_dict(conf)

    def test_text(self):
        conf: SomeConfig = SomeConfig.loads(json.dumps(test_dict))
        verify_test_dict(conf)

    def test_environ(self):
        os.environ['ENVVAR'] = 'hmm'
        conf: SomeConfig = SomeConfig.parse_dict(env_dict)
        verify_test_dict(conf)
