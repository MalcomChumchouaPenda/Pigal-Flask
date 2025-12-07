
import os
import sys
from flask_restx import Api
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


class PigalApi(Api):
    pass



# class PigalApi(Namespace):
#     """
#     The Extended Flask-Restx Namespace for Pigal Projects backend

#     Parameters
#     ----------
#     import_name: str
#         name used during import

#     """

#     def __init__(self, imported_file):
#         # split path components
#         path_components = []
#         current_file = imported_file
#         while current_file != os.path.dirname(current_file):
#             path_components.append(os.path.basename(current_file))
#             current_file = os.path.dirname(current_file)
#         path_components.append(current_file)
#         path_components.reverse()

#         # search root name
#         i = path_components.index('routes.py')
#         root_name = path_components[i-1]
#         super().__init__(root_name)

#     # @classmethod
#     # def login_required(cls, f):
#     #     """Décorateur pour protéger les routes API."""
#     #     @wraps(f)
#     #     def decorated_function(*args, **kwargs):
#     #         if not current_user.is_authenticated:
#     #             return {'message': 'Unauthorized'}, 401
#     #         return f(*args, **kwargs)
#     #     return decorated_function
    
#     # @classmethod
#     # def roles_accepted(cls, *roles):
#     #     """Décorateur pour protéger les routes API avec des rôles spécifiques."""
#     #     def decorator(f):
#     #         @wraps(f)
#     #         # @login_required
#     #         def decorated_function(*args, **kwargs):
#     #             if not current_user.is_authenticated:
#     #                 return {'message': 'Unauthorized'}, 401
#     #             if len([n for n in roles if current_user.has_role(n)]) == 0:
#     #                 return {'message': 'Forbidden'}, 403
#     #             return f(*args, **kwargs)
#     #         return decorated_function
#     #     return decorator
