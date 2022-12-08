import re
from pathlib import Path
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

path = Path(__file__).parent / "lanyard" / "__init__.py"
version = re.search(r'\d[.]\d[.]\d',path.read_text())[0]

packages = [
    'lanyard',
]


setup(
    name='lanyard.py',
    author='SawshaDev',
    version=version,
    packages=packages,
    license='MIT',
    description='An asynchronous python impl of the Lanyard API and Gateway!',
    install_requires=requirements,
    python_requires='>=3.8.0',
)