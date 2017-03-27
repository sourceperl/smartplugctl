from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='smartplugctl',
    version='0.0.5',
    license='MIT',
    url='https://github.com/sourceperl/smartplugctl',
    platforms='any',
    install_requires=required,
    py_modules=[
        'pySmartPlugSmpB16'
    ],
    scripts=[
        'scripts/smartplugctl',
        'scripts/smartplugscan'
    ]
)
