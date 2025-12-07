
import os
import sys
# from sqlalchemy.orm import declared_attr


def __find_key(cls):
    module = sys.modules[cls.__module__]
    root_path = os.path.abspath(module.__file__)
    while 'models' in root_path:
        root_path = os.path.dirname(root_path)
    return os.path.basename(root_path)
    
# @declared_attr
# def bind_key(cls):
#     return __find_key(cls)
    
# @declared_attr
# def tablename(cls):
#     key = __find_key(cls)
#     name = cls.__name__.lower()
#     return f'{key}_{name}'