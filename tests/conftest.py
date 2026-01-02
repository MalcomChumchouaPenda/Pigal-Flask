
import os
import sys

root_dir = os.path.dirname(__file__)
while 'tests' in root_dir:
    root_dir = os.path.dirname(root_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)


import pytest
from contextlib import contextmanager

@contextmanager
def _change_dir(new_dir):
    old_dir = os.getcwd()
    try:
        os.chdir(new_dir)
        yield
    finally:
        os.chdir(old_dir)

@pytest.fixture
def change_dir():
    return _change_dir
