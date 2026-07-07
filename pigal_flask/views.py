
import os
from flask import Blueprint


class WebUi(Blueprint):
    """A Web User Interface for a module or domain.
    
    This is a extended Flask Blueprint whose name and url_prefix are automatically generated.
    It is automatically detected during app loading. It is required for web routing.

    Parameters:
        views_file: The filepath of related views

    """

    def __init__(self, views_file):
        # split path components
        path_components = []
        current_file = views_file
        while current_file != os.path.dirname(current_file):
            path_components.append(os.path.basename(current_file))
            current_file = os.path.dirname(current_file)
        path_components.append(current_file)
        path_components.reverse()

        # search root name
        i = path_components.index('views.py')
        root_name = path_components[i-1]

        # search import name
        j = path_components.index('modules')
        import_parts = path_components[j:]
        import_parts[-1] = import_parts[-1].replace(".py", "")
        import_name = ".".join(import_parts)

        # calcul url_prefix
        url_prefix = '/'
        if root_name not in ['home', 'auth']:
            url_prefix += root_name

        # search static url
        static_url_path = os.path.join(*path_components[:i])
        static_url_path = os.path.join(static_url_path, 'assets')
        super().__init__(root_name, 
                         import_name, 
                         url_prefix=url_prefix,
                         template_folder='pages', 
                         static_folder=static_url_path,
                         static_url_path=static_url_path)
        
        
    def route(self, rule, **options):
        def decorator(cls):
            if hasattr(cls, 'methods'):
                methods = cls.methods
            else:
                methods = [
                    name.upper()
                    for name in ("get", "post", "put", "patch", "delete")
                    if hasattr(cls, name)
                ]

            print(cls, rule, options)
            self.add_url_rule(
                rule,
                cls.__name__.lower(),
                cls.as_view(cls.__name__.lower()),
                methods=methods
            )
            return cls
        return decorator
    

class FileView:
    """ A File-based routing view for module/domain

    This is View which implement file-based routing for a module Ui.
    """

# ui = Blueprint('x', __file__)

# @ui.route('/hello')
# class Demo:
#     def get(self):
#         return 'Hello World'