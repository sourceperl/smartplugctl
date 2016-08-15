from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    license='MIT',
    url='https://github.com/sourceperl/smartplugctl/python_module',
    platforms='any',
    install_requires=required,
    py_modules=[
        'pySmartPlugSmpB16',
    ]
)
