from setuptools import setup, find_packages

find_packages

with open('configlib/version.py') as f:
    _loc, _glob = {}, {}
    exec(f.read(), _loc, _glob)
    version = {**_loc, **_glob}['VERSION']

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('requirements-dev.txt') as f:
    dev_requirements = f.read().splitlines()

with open('README.md') as f:
    readme = f.read()

if not version:
    raise RuntimeError('version is not set in configlib/version.py')

setup(
    name="configlib",
    author="romangraef",
    url="https://github.com/romangraef/configlib",
    version=str(version),
    install_requires=requirements,
    long_description=readme,
    setup_requires=['pytest-runner', 'pytest-pylint'],
    tests_require=['pytest', 'pylint'],
    license="MIT",
    extras_require={
        'dev': dev_requirements,
    },
    packages=['configlib'],
    description="An easy python config manager",
    classifiers=[
        'Topic :: Utilities',
    ]
)
