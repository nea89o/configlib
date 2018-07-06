Configlib
=========

An easy python config library. Manage multiple configuration environments and complex nested configurations with ease.

Examples
--------
```json
{
    "config_var": "jo",
    "other_var": 3,
    "SubConfig": {
        "subconfivar": 10
    }
}
```


```py
from configlib import BaseConfig


class Config(BaseConfig):
    config_var: str
    other_var: int
    class SubConfig:
        subconfigvar: int

# Usage

config = Config.get_instance()
config.config_var # "jo"
config.SubConfig.subconfigvar # 10
```

Other Features
--------------

Having multiple config environments inheriting properties from each other, loading data from environment variables, etc.