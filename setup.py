from setuptools import setup

setup(
    name="typemedaddy",
    version="0.2",
    packages=["typemedaddy"],
    author="Witold Zolnowski",
    description="Derives type hints from data captured during runtime. Updates source files with type hints. USE SOURCE CONTROL before using!!!!",
    install_requires=["autopep8>=2.0.0"],
)
