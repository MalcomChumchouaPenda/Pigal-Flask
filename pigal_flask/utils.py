
import os
import re
import sys
from pathlib import Path
from flask import Blueprint
from flask_restx import Namespace
from sqlalchemy.orm import declared_attr


class TestUI:
    pass


def __find_key(cls):
    name_parts = cls.__module__.split('.')
    i = name_parts.index('models')
    return name_parts[i-1]
    
@declared_attr
def bind_key(cls):
    return __find_key(cls)
    
@declared_attr
def tablename(cls):
    key = __find_key(cls)
    name = cls.__name__.lower()
    return f'{key}_{name}'

