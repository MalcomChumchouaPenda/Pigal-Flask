
import os
import sys
from flask import Blueprint
from flask_restx import Namespace
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


class PigalUi(Blueprint):
    pass

class PigalApi(Namespace):
    pass




# class PigalUi(Blueprint):
#     """
#     The Extended Flask Blueprint for Pigal Projects frontend

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
#         if 'routes' in path_components:
#             i = path_components.index('routes')
#         else:
#             i = path_components.index('routes.py')
#         root_name = path_components[i-1]

#         # search import name
#         j = path_components.index('pages')
#         import_parts = path_components[j:]
#         import_parts[-1] = import_parts[-1].replace(".py", "")
#         import_name = ".".join(import_parts)

#         # search static url
#         static_url_path = os.path.join(*path_components[:i])
#         static_url_path = os.path.join(static_url_path, 'static')
#         super().__init__(root_name, import_name, 
#                          template_folder='templates', 
#                          static_folder='static',
#                          static_url_path=static_url_path)
#         # self.login_required = login_required


#     # def roles_accepted(self, *roles):
#     #     """Décorateur pour protéger les routes Flask qui renvoient des pages HTML."""
#     #     def decorator(f):
#     #         @wraps(f)
#     #         @login_required
#     #         def decorated_function(*args, **kwargs):
#     #             if not current_user.is_authenticated:
#     #                 # Redirection vers la page de connexion
#     #                 msg = "Vous devez être connecté pour accéder à cette page."
#     #                 return redirect(url_for('home.login', message=msg))  
#     #             if len([n for n in roles if current_user.has_role(n)]) == 0:
#     #                  # Redirection vers la page d'accueil
#     #                 msg = "Vous n'avez pas la permission d'accéder à cette page."
#     #                 return redirect(url_for('home.access_denied', message=msg)) 
#     #             return f(*args, **kwargs)
#     #         return decorated_function
#     #     return decorator


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
