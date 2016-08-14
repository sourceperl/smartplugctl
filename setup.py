from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    license='MIT',
    url='https://github.com/sourceperl/smartplugctl',
    platforms='any',
    install_requires=required,
    scripts=[
        'scripts/smartplugctl'
    ]
)
