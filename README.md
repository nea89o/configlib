Configlib
=========

An easy python config library. Manage multiple configuration environments and complex nested configurations with ease.

Examples
--------
```json
{
    "config_var": "jo",
    "other_var": 3,
    "subConfig": {
        "subconfigvar": 10
    }
}
```


```py
from configlib import BaseConfig

class SubConfig(object):
    subconfigvar: int

class Config(BaseConfig):
    config_var: str
    other_var: int
    subConfig: SubConfig

# Usage

config = Config.get_instance()
config.config_var # "jo"
config.SubConfig.subconfigvar # 10
```

Other Features
--------------

Having multiple config environments inheriting properties from each other, loading data from environment variables, etc.